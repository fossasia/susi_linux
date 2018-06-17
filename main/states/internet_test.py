""" Function to test the internet connection
"""
import urllib2


def internet_on():
        try:
            urllib2.urlopen('http://216.58.192.142', timeout=1)  # nosec #pylint-disable type: ignore
            return True  # pylint-enable
        except urllib2.URLError as err:
            print(err)
            return False
