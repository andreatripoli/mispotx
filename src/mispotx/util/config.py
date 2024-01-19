import configparser
import sys


class Config:
    api_key_alienvault = None
    timestamp_alienvault = None
    api_key_misp = None
    instance_misp = None
    log = None
    config = None

    def __init__(self, log, config, path):
        try:
            # Trying to read the configuration file
            self.log = log
            self.config = config
            self.config.read(path)


            # Checking if the configuration file is empty (not present)
            if not config.sections():
                log.error((f"The configuration file 'config.ini' was not found."))
                sys.exit(13)

        except FileNotFoundError:
            log.error("The configuration file 'config.ini' was not found.")
            sys.exit(13)
        except configparser.NoSectionError as e:
            log.error(f"Error in configuration file section: '{e}")
            sys.exit(13)
        except configparser.NoOptionError as e:
            log.error(f"Error in configuration file option: '{e}")
            sys.exit(13)

    # Get API OTX
    def get_api_key_alienvault(self):
        self.api_key_alienvault = self.config.get(section='AlienVault', option='api_key')
        if self.api_key_alienvault == "API":
            self.log.warning(f"You need to set up the OTX API")
            sys.exit(12)
        return self.api_key_alienvault

    # Get Timestamp AlienVault
    def get_timestamp(self):
        self.timestamp_alienvault = self.config.get(section='AlienVault', option='timestamp')
        if self.timestamp_alienvault == "TIMESTAMP":
            self.log.warning(f"You need to set up the Timestamp")
            sys.exit(12)
        return self.timestamp_alienvault

    # Set Timestamp AlienVault
    def set_timestamp(self, timestamp, path=None):
        try:
            self.config.set(section='AlienVault', option='timestamp', value=timestamp)
            with open(path, 'w') as configfile:
                self.config.write(configfile)
        except:
            self.log.warning(f"Error updating timestamp")

    # Get Instance MISP
    def get_instance_misp(self):
        self.instance_misp = self.config.get(section='MISP', option='misp_instance')
        if self.instance_misp == "INSTANCE":
            self.log.warning(f"You need to set up the MISP Instance")
            sys.exit(12)
        return self.instance_misp

    # Get API MISP
    def get_api_key_misp(self):
        self.api_key_misp = self.config.get(section='MISP', option='api_key')
        if self.api_key_misp == "API":
            self.log.warning(f"You need to set up the MISP API")
            sys.exit(12)
        return self.api_key_misp

    # Write config.ini
    def set_config(self, api_key_alienvault = None, timestamp_alienvault = None, api_key_misp = None,
                   instance_misp = None, path=None):
        try:
            # Checking if the configuration file is empty (not present)
            if not self.config.sections():
                raise FileNotFoundError(f"The configuration file 'config.ini' was not found.")

            # Writing values
            if api_key_alienvault is not None:
                self.config.set(section='AlienVault', option='api_key', value=api_key_alienvault)
                self.api_key_alienvault = api_key_alienvault

            if api_key_misp is not None:
                self.config.set(section='MISP', option='api_key', value=api_key_misp)
                self.api_key_misp = api_key_misp

            if instance_misp is not None:
                self.config.set(section='MISP', option='misp_instance', value=instance_misp)
                self.instance_misp = instance_misp

            if timestamp_alienvault is not None:
                self.config.set(section='AlienVault', option='timestamp', value=timestamp_alienvault)
                self.timestamp_alienvault = timestamp_alienvault

            # Saving changes
            with open(path, 'w') as configfile:
                self.config.write(configfile)

        except FileNotFoundError:
            self.log.error("The configuration file 'config.ini' was not found.")
            sys.exit(14)
        except configparser.NoSectionError as e:
            self.log.error(f"Error in configuration file section: '{e}")
            sys.exit(14)
        except configparser.NoOptionError as e:
            self.log.error(f"Error in configuration file option: '{e}")
            sys.exit(14)