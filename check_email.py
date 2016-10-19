# Check email script
# @rdar
# taken from https://pythonadventures.wordpress.com/2012/09/08/check-gmail-for-new-messages/

import urllib2

FEED_URL = 'https://mail.google.com/mail/feed/atom'

def get_unread_msgs(user, passwd):
    username = '{user}@gmail.com'.format(user=user)
    p = urllib2.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, FEED_URL, username, passwd)
    auth_handler = urllib2.HTTPBasicAuthHandler(p)
    #auth_handler.add_password(
    #   realm='New mail feed',
    #   uri='https://mail.google.com',
    #   user='{user}@gmail.com'.format(user=user),
    #   passwd=passwd
    #)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    feed = urllib2.urlopen(FEED_URL)
    return feed.read()

##########

if __name__ == "__main__":
    import getpass

    user = raw_input('Username: ')
    passwd = getpass.getpass('Password: ')
    print get_unread_msgs(user, passwd)
