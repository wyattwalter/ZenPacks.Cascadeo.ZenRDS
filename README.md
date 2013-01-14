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

II. Install Zenpack 
1. Download the latest ZenPack here (attach link) 
2. Login to your Zenoss instance. 
3. Go to Advanced 
4. Under Settings, select Zenpacks. 
5. Click the gear button and select "Install Zenpack" 
6. Locate ZenPacks.Cascadeo.ZenRDS. Upload. Click OK to install. 
7. Restart the zopectl daemon. 
8. In Advanced -> Settings -> Daemons, click the restart button for Zopectl daemon. 
9. Wait for a few seconds and reload the Zenoss UI,

III. Add your devices to /Server/RDS 
1. The Zenpack will create /Server/RDS device class. 
2. Put all RDS intances you want to monitor in /Server/RDS (under infrastructure tab)
3. Disable Ping and SNMP monitoring for the device class.

IV. Configure instance names and secret keys 
1. Go to the "Configuration Properties" for the devie 
2. Set the following fields: zRDSIdentity (your AWS identity number), zRDSKey (your AWS secret key) and zRDSInstance (the instance name of the RDS - this is the first column in the AWS RDS Console). Make sure that the key has at least read-only privilge to the RDS instance.
3. Wait for the data to come in. 
4. Configure threshold levels according to your need in the ZenRDS template.


== Known Issues/Errors ==
* Error importing Boto module. This is a pre-requisite.
- Make sure that zenoss' python environment has access to the Boto library.
* 
