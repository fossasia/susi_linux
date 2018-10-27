""" Function to test the internet connection
"""
import urllib.request
from urllib import URLError


def internet_on():
        try:
            urllib.request.urlopen('http://216.58.192.142', timeout=1)  # nosec #pylint-disable type: ignore
            return True  # pylint-enable
        except URLError as err:
            print(err)
            return False
