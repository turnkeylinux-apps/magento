#!/usr/bin/python
"""Set Magento admin password, email, domain and auth keys

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=www.example.com
"""

import sys
import getopt
import inithooks_cache

import shutil
import hashlib

import pwd
import grp
import os
import executil

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_DOMAIN="www.example.com"
AUTHKEY_MESSAGE="""
Please enter your Magento Marketplace account %s key here (optional).
This is needed for upgrading the Magento installation through Composer.

The list of your account keys can be found at:
https://marketplace.magento.com/customer/accessKeys/list

Alternatively, you can leave this blank now and
configure your keys in the finished TurnKey Magento installation by
navigating to "System -> Enable Composer updates" in the sidebar.

You can also save the keys by invoking
'composer update'
in /var/www/magento or by creating an auth.json file manually.

Please see this URL for more information:
https://www.turnkeylinux.org/magento

"""

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain=',
                                        'privkey=', 'pubkey='])
    except getopt.GetoptError, e:
        usage(e)

    email = ""
    domain = ""
    password = ""
    privkey = ""
    pubkey = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--domain':
            domain = val
        elif opt == '--privkey':
            privkey = val
        elif opt == '--pubkey':
            pubkey = val

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

    inithooks_cache.write('APP_EMAIL', email)
    
    if not domain:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        domain = d.get_input(
            "Magento Domain",
            "Enter the domain to serve Magento.",
            DEFAULT_DOMAIN)

    if domain == "DEFAULT":
        domain = DEFAULT_DOMAIN

    inithooks_cache.write('APP_DOMAIN', domain)

    if not privkey:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        privkey = d.inputbox(
            "Magento Account Key",
            AUTHKEY_MESSAGE % 'private',
            '',
            'OK',
            'Skip')[1]

    if not pubkey:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        pubkey = d.inputbox(
            "Magento Account Key",
            AUTHKEY_MESSAGE % 'public',
            '',
            'OK',
            'Skip')[1]

    salt = executil.getoutput("grep key /var/www/magento/app/etc/env.php | cut -d\\\' -f 4")

    hashpass = hashlib.sha256(salt + password).hexdigest() + ':' + salt + ':1'

    m = MySQL()
    m.execute('UPDATE magento.admin_user SET email=\"%s\" WHERE username=\"admin\";' % email)
    m.execute('UPDATE magento.admin_user SET password=\"%s\" WHERE username=\"admin\";' % hashpass)
    m.execute('UPDATE magento.core_config_data SET value=\"http://%s/\" WHERE path=\"web/unsecure/base_url\";' % (domain))
    m.execute('UPDATE magento.core_config_data SET value=\"https://%s/\" WHERE path=\"web/secure/base_url\";' % (domain))

    # delete cache so it will be rebuilt for new domain
    shutil.rmtree("/var/www/magento/var/cache", ignore_errors=True)

    # write auth
    authfile = '/var/www/magento/auth.json'
    with open(authfile, 'w') as f:
        f.write('{"http-basic": {"repo.magento.com": {"username": "%s", "password": "%s"}}}' % (pubkey, privkey))

    uid = pwd.getpwnam('www-data').pw_uid
    gid = grp.getgrnam('www-data').gr_gid

    os.chown(authfile, uid, gid)

if __name__ == "__main__":
    main()

