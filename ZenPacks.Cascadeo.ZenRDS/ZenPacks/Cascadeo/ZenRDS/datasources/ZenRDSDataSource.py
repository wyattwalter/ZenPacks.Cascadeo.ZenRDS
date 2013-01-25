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
        {'id':'identity', 'type':'password', 'mode':'w'},
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
            parts.append('-I %s' % self.identity)
        if self.key:
            parts.append('-S %s' % self.key)
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
