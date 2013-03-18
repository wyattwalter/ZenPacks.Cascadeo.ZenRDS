###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2008, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__='''ZenRDSDataSource.py

Defines datasource for ZenRDS
'''

from Globals import InitializeClass

import Products.ZenModel.BasicDataSource as BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine

import os


class ZenRDSDataSource(ZenPackPersistence,
                                BasicDataSource.BasicDataSource):
    
    ZEN_RDS = 'ZenRDS'

    ZENPACKID = 'ZenPacks.Cascadeo.ZenRDS'

    sourcetypes = (ZEN_RDS,)
    sourcetype = ZEN_RDS

    parser = 'Nagios'

    timeout = 15
    eventClass = '/Status/RDS'

    instance = '${here/zRDSInstance}'
    identity = '${here/zRDSIdentity}'
    key = '${here/zRDSKey}'
    region = '${here/zRDSRegion}'

    _properties = BasicDataSource.BasicDataSource._properties + (
        {'id':'instance', 'type':'string', 'mode':'w'},
        {'id':'identity', 'type':'string', 'mode':'w'},
        {'id':'key', 'type':'password', 'mode':'w'},
        {'id':'region', 'type':'string', 'mode':'w'},
        )
        
    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.BasicDataSource.__init__(self, id, title,
                buildRelations)

    def useZenCommand(self):
        return True


    def getCommand(self, context):
        parts = ['check_rds.py']
        if self.identity:
            parts.append("-I '%s'" % self.identity)
        if self.key:
            parts.append("-S '%s'" % self.key)
        if self.instance:
            parts.append("-N '%s'" % self.instance)
        if self.region:
            parts.append("-R '%s'" % self.region)
        cmd = ' '.join(parts)
        cmd = BasicDataSource.BasicDataSource.getCommand(self, context, cmd)
        return cmd


    def checkCommandPrefix(self, context, cmd):
        if self.usessh:
            return os.path.join(context.zCommandPath, cmd)
        zp = self.getZenPack(context)
        return zp.path('libexec', cmd)


    def addDataPoints(self):
        dps = (
            ('AllocatedStorage', 'GAUGE'),
            ('CPUUtilization', 'GAUGE'),
            ('DatabaseConnections', 'GAUGE'),
            ('DiskUsage', 'GAUGE'),
            ('FreeableMemory', 'GAUGE'),
            ('FreeStorageMemory', 'GAUGE'),
            ('PercentDiskUsage', 'GAUGE'),
            ('ReadIOPS', 'GAUGE'),
            ('ReadLatency', 'GAUGE'),
            ('ReadThroughput', 'GAUGE'),
            ('StorageSize', 'GAUGE'),
            ('SwapUsage', 'GAUGE'),
            ('WriteIOPS', 'GAUGE'),
            ('WriteLatency', 'GAUGE'),
            ('WriteThroughput', 'GAUGE'),
        )
        for dpd in dps:
            dp = self.manage_addRRDDataPoint(dpd[0])
            dp.rrdtype = dpd[1]
            dp.rrdmin = 0

InitializeClass(ZenRDSDataSource)
