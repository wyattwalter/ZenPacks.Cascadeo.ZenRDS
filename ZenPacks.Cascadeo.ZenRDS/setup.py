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

################################
# These variables are overwritten by Zenoss when the ZenPack is exported
# or saved.  Do not modify them directly here.
# NB: PACKAGES is deprecated
NAME = "ZenPacks.Cascadeo.ZenRDS"
VERSION = "1.0"
AUTHOR = "jerome@cascadeo.com"
LICENSE = ""
NAMESPACE_PACKAGES = ['ZenPacks', 'ZenPacks.Cascadeo']
PACKAGES = ['ZenPacks', 'ZenPacks.Cascadeo', 'ZenPacks.Cascadeo.ZenRDS']
INSTALL_REQUIRES = []
COMPAT_ZENOSS_VERS = ""
PREV_ZENPACK_NAME = ""
# STOP_REPLACEMENTS
################################
# Zenoss will not overwrite any changes you make below here.

from setuptools import setup, find_packages

setup(
    # This ZenPack metadata should usually be edited with the Zenoss
    # ZenPack edit page.  Whenever the edit page is submitted it will
    # overwrite the values below (the ones it knows about) with new values.
    name = NAME,
    version = VERSION,
    author = AUTHOR,
    license = LICENSE,
    
    # This is the version spec which indicates what versions of Zenoss
    # this ZenPack is compatible with
    compatZenossVers = COMPAT_ZENOSS_VERS,
    
    # previousZenPackName is a facility for telling Zenoss that the name
    # of this ZenPack has changed.  If no ZenPack with the current name is
    # installed then a zenpack of this name if installed will be upgraded.
    prevZenPackName = PREV_ZENPACK_NAME, 
    
    # Indicate to setuptools which namespace packages the zenpack
    # participates in
    namespace_packages = NAMESPACE_PACKAGES,
    
    # Tell setuptools what packages this zenpack provides.
    packages = find_packages(),
    
    # Tell setuptools to figure out for itself which files to include
    # in the binary egg when it is built.
    include_package_data = True,
    
    # The MANIFEST.in file is the recommended way of including additional files
    # in your ZenPack. package_data is another.
    #package_data = {}

    # Indicate dependencies on other python modules or ZenPacks.  This line
    # is modified by zenoss when the ZenPack edit page is submitted.  Zenoss
    # tries to put add/delete the names it manages at the beginning of this
    # list, so any manual additions should be added to the end.  Things will
    # go poorly if this line is broken into multiple lines or modified to
    # dramatically.
    install_requires = INSTALL_REQUIRES,

    # Every ZenPack egg must define exactly one zenoss.zenpacks entry point
    # of this form.
    entry_points = {
        'zenoss.zenpacks': '%s = %s' % (NAME, NAME),
    },

    # All ZenPack eggs must be installed in unzipped form.
    zip_safe = False,    
)
