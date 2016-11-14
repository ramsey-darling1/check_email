# Check email script
# @rdar
# taken from https://pythonadventures.wordpress.com/2012/09/08/check-gmail-for-new-messages/

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

def print_emails(user, passwd):
    xml = get_unread_msgs(user, passwd)
    o = untangle.parse(xml)
    try:
        print '****start****'
        print o.feed.title.cdata
        c = 0
        for e in o.feed.entry:
            title = e.title.cdata
            summary = e.summary.cdata
            print '***'
            print title
            print summary
            print 'from:'
            print e.author.name.cdata
            print e.author.email.cdata
            print '***'
            c += 1
        print str(c) + " new emails"
        print '****end******'
    except IndexError:
        print 'No New Mail'
        pass

def main():
    if(os.path.isfile("creds.xml") ):
        creds = untangle.parse("creds.xml")
        try:
            for a in creds.creds.account:
                user = a.username.cdata
                passwd = a.password.cdata
                print_emails(user, passwd)
        except ValueError:
            print "Sorry, unable to parse that xml file"
    else:
        user = raw_input('Username: ')
        passwd = getpass.getpass('Password: ')
        print_emails(user, passwd)

if __name__ == "__main__":
    main()
