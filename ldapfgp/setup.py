#!/usr/bin/env python

from setuptools import setup, find_packages

PACKAGE = 'LdapFgp'
VERSION = '0.1.0'

setup (
    name = PACKAGE,
    version = VERSION,
    description = 'LDAP Fine Grained Permission Extensions for Trac',
    author = 'Ilias Lazaridis',
    author_email = 'ilias@lazaridis.com',
    license='BSD', 
    url='https://github.com/lazaridis-com/ldaptrac',
    keywords = "trac ldap permission group acl OpenLDAP",
    install_requires = [ 'Trac>=0.12', 'Trac<0.13'],
    packages = find_packages(exclude=['ez_setup', '*.tests*']),
    package_data = { },
    entry_points = {
        'trac.plugins': [
            'ldapfgp.patch = ldapfgp.patch',
        ]
    }
)
