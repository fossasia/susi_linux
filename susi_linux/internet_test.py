"""
Function to test the internet connection
"""
import logging
import urllib.request
from urllib.error import URLError


logger = logging.getLogger(__name__)


def internet_on():
    url = 'http://216.58.192.142'
    try:
        # nosec #pylint-disable type: ignore
        urllib.request.urlopen(url, timeout=1)
        return True  # pylint-enable
    except URLError as err:
        logger.error("Test %s failed. Error: %s", url, err)
        return False
