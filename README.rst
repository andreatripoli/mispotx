.. mispotx documentation master file, created by
   sphinx-quickstart on Wed Jan 17 19:59:16 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation!
===================================
.. raw:: html

   <!-- PROJECT LOGO -->
   <br />
   <div style="text-align:center;">
     <h2 style="text-align:center; letter-spacing: .2rem;">MISPOTX</h2>

     <p style="text-align:center;">
       A tool to push OTXs to MISP!
       <br />
       <a href="https://mispotx.readthedocs.io/en/latest/"><strong>Explore the docs »</strong></a>
       <br />
       <br />
       <a href="https://github.com/andreatripoli/mispotx/issues">Report Bug</a>
       ·
       <a href="https://github.com/andreatripoli/mispotx/issues">Request Feature</a>
     </p>
   </div>
   <br><br><br>


==================
About The Project
==================

**MISPOTX** was born from the need to import pulls (otx) from the AlienVault platform onto your MISP instance, trying to maintain the original features as much as possible.



********************
Built With
********************

This section lists all the major frameworks/libraries used to start the project.

* .. image:: https://img.shields.io/badge/Python-3.12-green
   :width: 90
   :alt: Python 3.12

* .. image:: https://img.shields.io/badge/OTXv2-1.5.12-purple
   :width: 90
   :alt: OTXv2 1.5.12

* .. image:: https://img.shields.io/badge/PyMISP-2.4.183-blue
   :width: 90
   :alt: PyMISP 2.4.183


================
Getting Started
================

Installing **MISPOTX** is quite simple and below I offer you a guide for installation and use.

********************
Prerequisites
********************
Before proceeding with the installation, you need to make sure you have the AlienVault and MISP API Keys.

* AlienVault
    * Go to https://otx.alienvault.com/
    * *Login* or *Register* (if you are not)
    * Go to *Settings* and then *Api Integration*
    * Copy the value of **Your OTX Key**

* MISP
    * Log in to your MISP instance
    * Generate and copy the API relating to a user (contact the administrator if necessary)

********************
Installation
********************

To install **MISPOTX** follow the steps below.

1. Open the terminal and type

    ::

        pip install mispotx


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


    The first three fields are mandatory. The timestamp, if you don't set it the first time, will take all the OTXs.
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

* **-n** (no-publish) It allows you to choose whether to publish events or not (default False)
* **-a** (no-author) Allows you to choose whether to put the author's name in the Title/Info field (default False)
* **-no-tlp** (no-tlp) Allows you to choose whether to include the tlp in the tags (default False)
* **--distribution** (--distribution) Allows you to choose with which distribution to publish events (default organisation)
* **--threat-level** (--threat-level) It allows you to choose at what threat level to publish events (default undefined)
* **--analysis** (--analysis) It allows you to choose with which level of analysis to publish events (default completed)



========
Roadmap
========


.. |check_| raw:: html

    <input checked=""  disabled="" type="checkbox">

.. |uncheck_| raw:: html

    <input disabled="" type="checkbox">



|check_| Upgrade PyMISP to version 2.4.183

|check_| Upgrade OTXv2 to version 1.5.12

|check_| Extrapolation Features

|check_| Creation of tools to import pulls onto the MISP instance

|uncheck_| Update the event (I'm looking for an effective method to update)


========
License
========

Distributed under the MIT License. See `LICENSE <https://github.com/andreatripoli/mispotx/LICENSE>`_ for more information.


========
Contact
========

Andrea Tripoli

Project Link: https://github.com/andreatripoli/mispotx


================
Acknowledgments
================

I have included the materials (projects and manuals) that helped me develop.

* https://github.com/gitunique/cti-scripts/tree/master/otx-misp
* https://otx-misp.readthedocs.io
* https://pymisp.readthedocs.io/
* https://www.misp-project.org/
* https://otx.alienvault.com/

