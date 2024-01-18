================
OTX -> MISP
================

Below are all the mappings from OTX to MISP.

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - AlienVault OTX
     - MISP
   * - author_name + name
     - info
   * - created
     - date
   * - description
     - comment
   * - tlp
     - tag
   * - tags
     - tag
   * - adversary
     - threat-actor
   * - malware
     - malware-type
   * - country
     - target-location
   * - FileHash-SHA256 (indicator)
     - sha256
   * - FileHash-SHA256 (indicator)
     - sha256
   * - FileHash-SHA1 (indicator)
     - sha1
   * - FileHash-MD5 (indicator)
     - md5
   * - URL (indicator)
     - url
   * - domain (indicator)
     - domain
   * - hostname (indicator)
     - hostname
   * - IPv4/IPv6 (indicator)
     - ip-dst
   * - email (indicator)
     - email
   * - Mutex (indicator)
     - mutex
   * - CVE (indicator)
     - vulnerability
   * - FileHash-IMPHASH (indicator)
     - impash
   * - FileHash-PEHASH (indicator)
     - pehash
   * - FilePath (indicator)
     - filename
   * - YARA (indicator)
     - yara
