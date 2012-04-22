#!/usr/bin/python
"""Set Magento admin password and email, and domain to serve

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=shop.example.com
"""

import sys
import getopt
import shutil
import hashlib

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_DOMAIN="shop.example.com"

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain='])
    except getopt.GetoptError, e:
        usage(e)

    email = ""
    domain = ""
    password = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--domain':
            domain = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Magento Password",
            "Enter new password for the Magento 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "Magento Email",
            "Enter email address for the Magento 'admin' account.",
            "admin@example.com")
    
    if not domain:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        domain = d.get_input(
            "Magento Domain",
            "Enter the domain to serve Magento.",
            DEFAULT_DOMAIN)

    if domain == "DEFAULT":
        domain = DEFAULT_DOMAIN

    hashpass = hashlib.md5("qX" + password).hexdigest() + ":qX"

    m = MySQL()
    m.execute('UPDATE magento.admin_user SET email=\"%s\" WHERE username=\"admin\";' % email)
    m.execute('UPDATE magento.admin_user SET password=\"%s\" WHERE username=\"admin\";' % hashpass)
    m.execute('UPDATE magento.core_config_data SET value=\"http://%s/\" WHERE path=\"web/unsecure/base_url\";' % (domain))
    m.execute('UPDATE magento.core_config_data SET value=\"https://%s/\" WHERE path=\"web/secure/base_url\";' % (domain))

    # delete cache so it will be rebuilt for new domain
    shutil.rmtree("/var/www/magento/var/cache", ignore_errors=True)

if __name__ == "__main__":
    main()

