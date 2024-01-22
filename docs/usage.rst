========
Usage
========

The use of **MISPOTX** consists of two phases: the first is setting the Keys and the second is executing the pull
download and uploading to the *MISP* instance.

* Key setting
    1. Open terminal and type
    ::

            mispotx -vv -w -o <OTX_API_KEY> -s <MISP_INSTANCE> -m <MISP_API_KEY> -t <TIMESTAMP>


    The previous command sets the variables in the config.ini file.

    * **-vv** Set verbosity (strongly recommended)
    * **-w** Write the config.ini file
    * **-o** Paste the AlienVault API Key
    * **-s** Paste the MISP INSTANCE (e.g. https://localhost.com)
    * **-m** Paste the MISP API Key
    * **-t** Paste the timestamp of the time from which you want to download the otx (e.g. 2024-01-01T03:40:26.627569)


    The first three fields are mandatory.
    **It is important to remember that every time the OTXs are downloaded, the timestamp is automatically updated with
    the latest event so that no OTX duplicates are created.**

* Download OTX and PUSH
    1. Once the first setup phase has been completed, it is possible to continue with the OTX download and the push to
    MISP. Then open the terminal and run the following command:
    ::

            mispotx -vv -c

    The **-c** option allows you to read the configuration of the *config.ini* file. In this way **MISPOTX** will
    download the OTXs and automatically push them to *MISP*.


********************
More options
********************

Below are the options provided by **MISPOTX**.

* **-n** (--no-publish) It allows you to choose whether to publish events or not (default False)
* **-a** (--no-author) Allows you to choose whether to put the author's name in the Title/Info field (default False)
* **-no-tlp** Allows you to choose whether to include the tlp in the tags (default False)
* **--distribution** Allows you to choose with which distribution to publish events (default organisation)
* **--threat-level** It allows you to choose at what threat level to publish events (default undefined)
* **--analysis** It allows you to choose with which level of analysis to publish events (default completed)


********************
Tips
********************

Here are some tips:

* It is recommended to set as much older than current in order to download all OTXs to date
* It is recommended, after setting the keys, to set the cronjob in order to schedule the download of the OTXs.
  The timestamp is automatically saved with the latest download to avoid duplicate OTX on MISP. This mechanism allows
  the cronjob to work
* Be careful because MISP event updating is not currently supported, so you run the risk of duplicate events if you
  enter the same timestamps. We are working to support it (uid)


