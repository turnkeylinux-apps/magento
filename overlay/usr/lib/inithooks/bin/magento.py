#!/usr/bin/python3
"""Set Magento admin password, email, domain and auth keys

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=www.example.com
    --privkey=  unless provided, will ask interactively
                DEFAULT=SKIP
    --pubkey=   unless provided, will ask interactively
                DEFAULT=SKIP
"""

import sys
import getopt
import inithooks_cache
import subprocess

import shutil
import hashlib

import pwd
import grp
import os

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s [options]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)

DEFAULT_DOMAIN="www.example.com"
AUTHKEY_MESSAGE="""
Please enter your Magento Marketplace account %s key here (optional). This is needed for upgrading the Magento installation via commandline. It is also required for third party integrations.

Keys can be added later if not provided now.

For more information, please see:
https://www.turnkeylinux.org/docs/magento

"""

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain=',
                                        'privkey=', 'pubkey='])
    except getopt.GetoptError as e:
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

    if privkey == "DEFAULT":
        privkey = "SKIP"

    if privkey and not pubkey:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        pubkey = d.inputbox(
            "Magento Account Key",
            AUTHKEY_MESSAGE % 'public',
            '',
            'OK',
            'Skip')[1]

    if pubkey == "DEFAULT":
        pubkey = "SKIP"

    salt = subprocess.check_output([
        "grep", "key", "/var/www/magento/app/etc/env.php"
    ], text=True).split("'")[3]

    hashpass = hashlib.sha256((salt + password).encode()).hexdigest() + ':' + salt + ':1'

    m = MySQL()
    m.execute('UPDATE magento.admin_user SET email=%s WHERE username=\"admin\";', (email,))
    m.execute('UPDATE magento.admin_user SET password=%s WHERE username=\"admin\";', (hashpass,))
    m.execute('UPDATE magento.core_config_data SET value=%s WHERE path=\"web/unsecure/base_url\";', (f'http://{domain}/',))
    m.execute('UPDATE magento.core_config_data SET value=%s WHERE path=\"web/secure/base_url\";', (f'https://{domain}/',))

    # delete cache so it will be rebuilt for new domain
    shutil.rmtree("/var/www/magento/var/cache", ignore_errors=True)

    # write auth
    if privkey != "SKIP" and pubkey != "SKIP":
        authfile = '/var/www/magento/auth.json'
        with open(authfile, 'w') as f:
            f.write('{"http-basic": {"repo.magento.com": {"username": "%s", "password": "%s"}}}' % (pubkey, privkey))

        uid = pwd.getpwnam('www-data').pw_uid
        gid = grp.getgrnam('www-data').gr_gid

        os.chown(authfile, uid, gid)

if __name__ == "__main__":
    main()

