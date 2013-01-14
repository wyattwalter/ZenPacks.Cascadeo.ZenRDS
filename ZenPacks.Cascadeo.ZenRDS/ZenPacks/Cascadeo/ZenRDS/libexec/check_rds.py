#!/usr/local/zenoss/zenoss/bin/python
import sys
import datetime
from optparse import OptionParser
try:
    import boto
except:
    print "Error importing Boto module. This is a pre-requisite."
    sys.exit(1)



class ZenossRDSPlugin:
    def __init__(self, instance, identity, secret):
        self.instance = instance
        self.identity = identity
        self.secret = secret

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
            self.rds = boto.connect_rds(self.identity, self.secret, validate_certs=False)
        except Exception, e:
            print "Boto Error: %s" % (e,)
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
    options, args = parser.parse_args()
    if not (options.instance and options.identity and options.secret):
        print "You must specify the instance, identity, secret parameters."
        sys.exit(1)

    cmd = ZenossRDSPlugin(options.instance, options.identity, options.secret)
    cmd.run()
    sys.exit(0)
