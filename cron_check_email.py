#!/usr/bin/env python
# Check email script
# @rdar
# This script is meant to be run from a cronjob

import urllib2
import untangle
import os.path
import getpass

FEED_URL = 'https://mail.google.com/mail/feed/atom'

def get_unread_msgs(user, passwd):
    username = '{user}@gmail.com'.format(user=user)
    p = urllib2.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, FEED_URL, username, passwd)
    auth_handler = urllib2.HTTPBasicAuthHandler(p)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    feed = urllib2.urlopen(FEED_URL)
    return feed.read()

def alert_emails(user, passwd):
    xml = get_unread_msgs(user, passwd)
    o = untangle.parse(xml)
    res = ''
    try:
        c = 0
        for e in o.feed.entry:
            c += 1
        res = str(c) + " new emails "
    except IndexError:
        # do nothing
        pass
    return res

def main():
    # nothing happens if the creds.xml file is not in place
    res = ''
    if(os.path.isfile("creds.xml") ):
        creds = untangle.parse("creds.xml")
        try:
            for a in creds.creds.account:
                user = a.username.cdata
                passwd = a.password.cdata
                res += alert_emails(user, passwd)
        except ValueError:
            # do nothing
            pass
    print res

if __name__ == "__main__":
    main()
