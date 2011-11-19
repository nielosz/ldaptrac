# -*- coding: utf-8 -*-
#
# LDAP permission extensions for Trac
# 
# Copyright (C) 2009 Lennert Van Alboon (http://vanalboom.org/node/15)
# Copyright (C) 2011 Ilias Lazaridis <ilias@lazaridis.com>
# All rights reserved.
#
# Dynapatch (monkeypatch) to avoid manual patching of
#
# Status: DRAFT, UNTESTED
#
#------------------------------------------------------------------------------

from trac.core import *
from trac.env import IEnvironmentSetupParticipant
from tracopt.perm.authz_policy import AuthzPolicy

#------------------------------------------------------------------------------

authz_permissions_old = AuthzPolicy.authz_permissions

def authz_permissions_patch():
    if AuthzPolicy.authz_permissions != authz_permissions_new:
        authz_permissions_old = AuthzPolicy.authz_permissions  
        AuthzPolicy.authz_permissions = authz_permissions_new

#------------------------------------------------------------------------------
    
class AuthsPolicyOnApacheLdap(Component):
    """ (draft) when enabled, altered Authz.authz_permissions is used
    """

    implements(IEnvironmentSetupParticipant)       

    # on Component activation, override existent method with new one
    def __init__(self):
        authz_permissions_patch()
        self.log.debug('authz_permissions patched')
        
#TODO trac:#4190 - replace dummies to force component initialization
    # IEnvironmentSetupParticipant    
    def environment_created(self):           pass
    def environment_needs_upgrade(self, db): return False
    def upgrade_environment(self, db):       pass

#---------------------------------

def authz_permissions_new(self, *args) :
    """
    Use alternative permission retrieval
    """
    
    # unverified code, taken from (http://vanalboom.org/node/15)
    
    #TD: verify code, possibly the reuse of original function
    #TD: verify overall logic, possibly use a modified permissionGroupProvider

    # original menthod not used
    #fields = authz_permissions_old(self, *args)
    
    if username and username != 'anonymous':
        valid_users = ['*', 'authenticated', username]
        perms = LdapPermissionGroupProvider(self.env).get_permission_groups(username)
        valid_users += perms
    else:
        valid_users = ['*', 'anonymous']
    for resource_section in self.authz.sections:
        resource_glob = to_unicode(resource_section)
        if '@' not in resource_glob:
            resource_glob += '@*'
        if fnmatch(resource_key, resource_glob):
            section = self.authz[resource_section]
            for who, permissions in section.iteritems():
                if who in valid_users:
                    if isinstance(permissions, basestring):
                        return [permissions]
                    else:
                        return permissions
                else:
                    self.log.debug('%s does not match any of valid_users: %s', who, valid_users)
    return None
    

#------------------------------------------------------------------------------
  

