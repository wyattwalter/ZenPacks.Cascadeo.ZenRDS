#!/usr/local/zenoss/zenoss/bin/python

#### Copyright (C) 2012-2013 Cascadeo Corporation
####
#### THE WORK (AS DEFINED BELOW) IS PROVIDED UNDER THE TERMS OF THIS 
#### CREATIVE COMMONS PUBLIC LICENSE ("CCPL" OR "LICENSE"). THE WORK IS 
#### PROTECTED BY COPYRIGHT AND/OR OTHER APPLICABLE LAW. ANY USE OF 
#### THE WORK OTHER THAN AS AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT 
#### LAW IS PROHIBITED.
####
#### BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT 
#### AND AGREE TO BE BOUND BY THE TERMS OF THIS LICENSE. TO THE EXTENT 
#### THIS LICENSE MAY BE CONSIDERED TO BE A CONTRACT, THE LICENSOR GRANTS 
#### YOU THE RIGHTS CONTAINED HERE IN CONSIDERATION OF YOUR ACCEPTANCE 
#### OF SUCH TERMS AND CONDITIONS.
####
#### Please see LICENSE for full legal details and the following URL
#### for a human-readable explanation:
####
#### http://creativecommons.org/licenses/by-nc-sa/3.0/us/
####

import sys
import datetime
from optparse import OptionParser
try:
    import boto
    import boto.rds
except:
    print "Error importing Boto module. This is a pre-requisite."
    sys.exit(1)



class ZenossRDSPlugin:
    def __init__(self, instance, identity, secret, region):
        self.instance = instance
        self.identity = identity
        self.secret = secret
	self.region = region

        self.metrics = ["CPUUtilization",
                        "DatabaseConnections",
                        "FreeableMemory",
                        "FreeStorageSpace",
                        "ReadIOPS",
                        "ReadLatency", 
                        "ReadThroughput", 
                        "SwapUsage", 
                        "WriteIOPS", 
                        "WriteLatency", 
                        "WriteThroughput",]

    def run(self):
        end =  datetime.datetime.utcnow()
        start = end - datetime.timedelta(minutes=5)

        try:
            self.cw = boto.connect_cloudwatch(self.identity, self.secret, validate_certs=False)
	    self.rds = None
            regions = boto.rds.regions()
            for r in regions:
                if r.name == self.region:
                    self.rds = boto.connect_rds(self.identity, self.secret, region=r, validate_certs=False)
        except Exception, e:
            print "Boto Error: %s" % (e,)
            sys.exit(1)

	if self.rds is None:
	    print "Boto Error: Unknown region %s" % (self.region)
            sys.exit(1)


        #data = ""
        data ={}
        for metric in self.metrics:
            try:
                s = self.cw.get_metric_statistics(60,start, end, metric, "AWS/RDS", "Average", {'DBInstanceIdentifier': self.instance})
            except Exception, e:
		print "Boto Error: %s" % (e,)
		sys.exit(1)

            if (len(s) != 0):
                data[metric] = s[len(s)-1]['Average']

        # Get allocated storage for RDS instance
        try:
	        inst = self.rds.get_all_dbinstances(self.instance)
        except Exception, e:
                print "Boto Error: %s" % (e,)
                sys.exit(1)

        if (len(inst) == 1):
            # Convert to GB
            data["AllocatedStorage"] = inst[0].allocated_storage * 1073741824

        #Calculate disk usage
        data["DiskUsage"] = data["AllocatedStorage"] - data["FreeStorageSpace"]
        data["PercentDiskUsage"] = (data["DiskUsage"] / data["AllocatedStorage"]) * 100

        status = " ".join(["%s=%s" % (k, v) for k, v in data.items()])
        print "STATUS OK| " + status

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-N', '--instance', dest='instance',
            help='RDS instance name')
    parser.add_option('-I', '--identity', dest='identity',
            help='AWS/RDS Identity')
    parser.add_option('-S', '--secret', dest='secret',
            help='AWS/RDS Secret')
    parser.add_option('-R', '--region', dest='region',
            help='AWS/RDS Region')
    options, args = parser.parse_args()
    if not (options.instance and options.identity and options.secret):
        print "You must specify the instance, identity, secret parameters."
        sys.exit(1)
 
    cmd = ZenossRDSPlugin(options.instance, options.identity, options.secret, options.region)
    cmd.run()
    sys.exit(0)
