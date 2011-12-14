Quickstart to test installation of openldap and ldapplugin, based on:
http://trac-hacks.org/wiki/LdapPluginTests 

---------------------------------------------------------------------


Install ldapplugin and dependencies
Install openldap

rename "sladp.conf" to "slapd-orig.conf"

Copy the file "slapd.conf" to your openldap installation, replacing the existent one.

$ mkdir ./db

With slapd stopped, copy "init.ldif" to your open-ldap installation and execute

$ slapadd -f slapd.conf -l init.ldif

start slapd, then run the test.

$ python ./ldapplugin/tests/api.py

if the the test passes, then things already work.

If the test fail, see the step-by-step instructions within:

http://trac-hacks.org/wiki/LdapPluginTests

Still problems, see for more info here:

http://trac-hacks.org/wiki/LdapPlugin
