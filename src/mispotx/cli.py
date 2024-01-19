import configparser
import os
import sys
import time
import logging
import argparse
from OTXv2 import OTXv2
from pymisp import PyMISP, MISPEvent, PyMISPError
from dateutil import parser as date_parser
from datetime import datetime

try:
    from utils import Config
except ImportError:
    from .utils import Config

log = logging.getLogger('mispotx')
console_handler = logging.StreamHandler()
log.addHandler(console_handler)

misp_distributions = ['organisation', 'community', 'connected', 'all']
misp_threat_levels = ['high', 'medium', 'low', 'undefined']
misp_analysis = ['initial', 'ongoing', 'completed']


def create_config_file(config_path):
    config = configparser.ConfigParser()

    # Add sections
    config['AlienVault'] = {'api_key': 'API', 'timestamp': 'TIMESTAMP'}
    config['MISP'] = {'misp_instance': 'INSTANCE', 'api_key': 'API'}

    with open(config_path, 'w') as config_file:
        config.write(config_file)

def get_config_path():
    # config.ini path
    config_path = os.path.join(os.path.dirname(__file__), "config.ini")

    # Create a file
    if not os.path.exists(config_path):
        create_config_file(config_path)

    return config_path


def get_misp_type(choices, bias=0):
    def misp_type(argument):
        try:
            dist = int(argument)
        except ValueError:
            argument = argument.lower()
            dist = choices.index(argument)
        if 0 <= dist < len(choices):
            return dist + bias
        raise ValueError

    return misp_type

# Argument Parser
parser = argparse.ArgumentParser(description='Downloads OTX pulses and create events on MISP.')
parser.add_argument('-o', '--otx', help="AlienVault OTX API key", dest='otx', default=None)
parser.add_argument('-s', '--server', help="MISP server URL", dest='server', default=None)
parser.add_argument('-m', '--misp', help="MISP API key", dest='misp', default=None)
parser.add_argument('-t', '--timestamp', help="Last import as Date/Time ISO format", dest='timestamp',
                    default=None)
parser.add_argument('-c', '--config-file', dest='config', action='store_false')
parser.add_argument('-w', '--write-config', help='Write the configuration file', action='store_true')
parser.add_argument('-n', '--no-publish', help="Don't publish the MISP event",
                    action='store_false', dest='publish')
parser.add_argument('-a', '--no-author', help='Delete the Pulse author name in the MISP Info field',
                    action='store_true')
parser.add_argument("-v", "--verbose", dest="verbose",
                    action="count", default=0,
                    help="Verbosity, repeat to increase the verbosity level.")
parser.add_argument('--no-tlp', help='No Traffic Light Protocol tag',
                    action='store_false', dest='tlp')
parser.add_argument('--distribution', help="MISP distribution of events ({}), default: {}"
                    .format(','.join(misp_distributions), misp_distributions[0]),
                    type=get_misp_type(misp_distributions), default=None)
parser.add_argument('--threat-level',
                    help="MISP threat level of events ({}), default: {}".format(','.join(misp_threat_levels),
                                                                                misp_threat_levels[3]),
                    type=get_misp_type(misp_threat_levels, bias=1), default=None)
parser.add_argument('--analysis',
                    help="MISP analysis state of events ({}), default: {}".format(','.join(misp_analysis),
                                                                                  misp_analysis[2]),
                    type=get_misp_type(misp_analysis), default=None)

def create_event(pulse=None, misp_api=None, distribution=0, threat_level=4, analysis=2, tlp=True, publish=True,
                 author=False):
    """
        :param pulse: List of Pulses as returned by `get_pulses`
        :param misp_api: MISP connection object
        :type misp_api: :class:`pymisp.PyMISP`
        :param distribution: distribution of the MISP event (0-4)
        :param threat_level: threat level of the MISP object (1-4)
        :param analysis: analysis stae of the MISP object (0-2)
        :param publish: Is the MISP event should be published?
        :type publish: Boolean
        :param tlp: Add TLP level tag to event
        :type tlp: Boolean
        :param author: Prepend the author to the Pulse name
        :type author: Boolean
        """
    try:
        mispEvent = MISPEvent()

        # Name of the event to create: author_name + name
        if not author:
            nameEvent = pulse['author_name'] + ' | ' + pulse['name']
        else:
            nameEvent = pulse['name']

        # Event date
        try:
            dt= date_parser.parse(pulse['created'])
            event_date = dt.strftime('%Y-%m-%d')
        except (ValueError, OverflowError):
            event_date = datetime.now().strftime('%Y-%m-%d')

        # Published date
        try:
            dt = datetime.strptime(pulse['modified'], "%Y-%m-%dT%H:%M:%S.%f")
            published_data = datetime.timestamp(dt)
        except (ValueError, OverflowError):
            published_data = datetime.timestamp(datetime.now())


        # Event setting (General)
        mispEvent.info = nameEvent
        mispEvent.analysis = analysis
        mispEvent.date = event_date
        mispEvent.distribution = distribution
        mispEvent.publish_timestamp = published_data
        mispEvent.threat_level_id = threat_level
        mispEvent.add_attribute(type="comment", value=pulse["description"], category='Other')

        if publish:
            mispEvent.publish()
        else:
            mispEvent.unpublish()

        # Event setting (TLP)
        if tlp:
            if 'TLP' in pulse:
                mispEvent.add_tag(pulse['TLP'])
            elif 'tlp' in pulse:
                mispEvent.add_tag(pulse['tlp'])

        # Event setting (TAGS)
        if pulse['tags']:
            for tag in pulse['tags']:
                mispEvent.add_tag(tag)

        # Event setting (Threat Actor)
        if pulse['adversary'] is not None:
            mispEvent.add_attribute('threat-actor', pulse['adversary'])

        # Event setting (Malware Type)
        if pulse['malware_families']:
            for malware in pulse['malware_families']:
                mispEvent.add_attribute('malware-type', malware)

        # Event setting (Targeted Countries)
        if pulse['targeted_countries']:
            for country in pulse['targeted_countries']:
                mispEvent.add_attribute("target-location", country)

        # Event setting (Indicators)
        for ind in pulse['indicators']:
            ind_type = ind['type']
            ind_val = ind['indicator']

            # Indicator: SHA256
            if ind_type == 'FileHash-SHA256':
                mispEvent.add_attribute("sha256", ind_val)

            # Indicator: SHA1
            elif ind_type == 'FileHash-SHA1':
                mispEvent.add_attribute("sha1", ind_val)

            # Indicator: MD5
            elif ind_type == 'FileHash-MD5':
                mispEvent.add_attribute("md5", ind_val)

            # Indicator: URL
            elif ind_type == 'URI' or ind_type == 'URL':
                mispEvent.add_attribute("url", ind_val)

            # Indicator: DOMAIN
            elif ind_type == 'domain':
                mispEvent.add_attribute("domain", ind_val)

            # Indicator: HOSTNAME
            elif ind_type == 'hostname':
                mispEvent.add_attribute("hostname", ind_val)

            # Indicator: IPV4/IPV6
            elif ind_type == 'IPv4' or ind_type == 'IPv6':
                mispEvent.add_attribute("ip-dst", ind_val)

            # Indicator: EMAIL
            elif ind_type == 'email':
                mispEvent.add_attribute("email", ind_val)

            # Indicator: MUTEX
            elif ind_type == 'Mutex':
                mispEvent.add_attribute("mutex", ind_val)

            # Indicator: CVE
            elif ind_type == 'CVE':
                mispEvent.add_attribute('vulnerability', ind_val)

            # Indicator: IMPHASH
            elif ind_type == 'FileHash-IMPHASH':
                mispEvent.add_attribute('imphash', ind_val)

            # Indicator: PEHASH
            elif ind_type == 'FileHash-PEHASH':
                mispEvent.add_attribute('pehash', ind_val, category='Artifacts dropped')

            # Indicator: FILEPATH
            elif ind_type == 'FilePath':
                mispEvent.add_attribute("filename", ind_val, category='Artifacts dropped')

            # Indicator: YARA
            elif ind_type == 'YARA':
                mispEvent.add_attribute("yara", ind_val, category='Artifacts dropped')

        # Add event to MISP
        result = misp_api.add_event(event=mispEvent)

        # Check errors
        if 'errors' in result:
            log.info("Errors: " + str(result['errors']))

        time.sleep(0.2)
    except Exception as e:
        log.error("Errors: " + str(e))


def main(args=None):
    # Check file
    config_path = get_config_path()

    config = configparser.ConfigParser()
    config.read(config_path)

    #Args
    args = parser.parse_args(args=args)
    if args.verbose == 1:
        log.setLevel('WARNING')
    elif args.verbose == 2:
        log.setLevel('INFO')
    elif args.verbose >= 3:
        log.setLevel('DEBUG')
    else:
        log.setLevel('ERROR')

    # Print config.ini
    for section in config.sections():
        log.info(f"[{section}]")
        for key, value in config.items(section):
            log.info(f"{key} = {value}")
        log.info("\n")

    # Check "config-file" option
    if not args.config and not args.write_config:
        # Get credentials
        credentials = Config(log=log, config=config, path=config_path)
    elif not args.config and args.write_config:
        log.error("Choice not allowed. Choose whether to write the configuration file or read the one you have"
              " already created (-c or -w)")
        sys.exit(10)

    else:
        # Set and Get credentials
        credentials = Config(log=log, config=config, path=config_path)
        credentials.set_config(api_key_alienvault=args.otx, timestamp_alienvault=args.timestamp,
                               api_key_misp=args.misp, instance_misp=args.server, path=config_path)

        log.info(f"Credentials set correctly. Now you can proceed to download the otxs and upload them to your MISP"
                 f" instance")
        sys.exit(13)

    try:
        # AlienVault OTX API
        otx = OTXv2(api_key=credentials.get_api_key_alienvault())

        # Get all pulses starting from timestamp
        pulses = otx.getsince(credentials.get_timestamp())
    except Exception as e:
        log.error("Error on OTX. Check the API")
        sys.exit(5)


    # Print the number of pulses recovered
    log.info("Retrieved {} pulses".format(len(pulses)))

    # Save the current date so you are updated
    credentials.set_timestamp(datetime.now().isoformat(), path=config_path)

    # PyMiSP API
    try:
        pymisp = PyMISP(url=credentials.get_instance_misp(), key=credentials.get_api_key_misp(), ssl=False)
    except PyMISPError as e:
        log.error("Cannot connect to MISP: '{}'".format(e.message))
        sys.exit(12)
    except Exception as e:
        ("Cannot connect to MISP, unknown exception: '{}'".format(str(e)))
        sys.exit(12)

    count = 0
    # Create single event
    for event in pulses:
        create_event(pulse=event, misp_api=pymisp, distribution=args.distribution, threat_level=args.threat_level,
                     analysis=args.analysis, tlp=args.tlp, publish=args.publish, author=args.no_author)
        log.info("Pulses left to push: {}".format(len(pulses)-count))
        count = count + 1