The ZenRDS ZenPack provides monitoring for AWS RDS instances without installing Zenoss AWS ZenPack. It provides the following performance metrics through CloudWatch API.

"CPUUtilization",
"DatabaseConnections",
"FreeableMemory",
"FreeStorageSpace",
"ReadIOPS",
"ReadLatency", 
"ReadThroughput", 
"SwapUsage", 
"WriteIOPS", 
"WriteLatency", 
"WriteThroughput"

To use Cascadeo ZenRDS Zenpack: 

I. Install Python-Boto on Zenoss Python environment

1. SSH in to Zenoss and login as zenoss user (important)
2. Download Python Boto library from http://boto.googlecode.com/files/
3. Untar and install it using python setup tools.

II. Install Zenpack Code from GitHub

1. On the zenoss host, clone the latest ZenRDS code 
2. Change directory to the zenpack's root dir.
3. Create egg package by executing `python setup.py bdist_egg`
4. Install the generated egg package/zenpack. `zenpack --install <Zenpackname.egg>`
5. Restart the zopectl and zeoctl daemons. 
6. Wait for a few seconds and reload the Zenoss UI,

III. Add your devices to /Server/RDS 

1. The Zenpack will create /Server/RDS device class. 
2. Put all RDS intances you want to monitor in /Server/RDS (under infrastructure tab)
3. <s>Disable Ping and SNMP monitoring for the device class.</s>

IV. Configure instance names and secret keys 

1. Go to the "Configuration Properties" for the devie 
2. Set the following fields: zRDSIdentity (your AWS identity number), zRDSKey (your AWS secret key), zRDSInstance (the instance name of the RDS) and zRDSRegion (region where the instance is us-east-1, us-west-1, etc). Make sure that the key has at least read-only privilge to the RDS instance.
3. Wait for the data to come in. Run zencommand to force collection.
4. Configure threshold levels according to your need in the ZenRDS template.


== Known Issues/Errors ==
* Error importing Boto module. This is a pre-requisite.
- Make sure that zenoss' python environment has access to the Boto library.
* Request has expired. Timestamp date: x-x-x-x
- Make sure that system time is accurate
