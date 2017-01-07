import urllib.request
import shutil
import argparse
import sys

# Taken from https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
# Required to bypass browser checking on livechart
USER_AGENT = {'User-Agent': 'Mozilla/5.0'}

def parse_args(args):
    """
    Parses the args for use in the script
    :param args: The arguments in a list
    :return: returns arguments that have been parsed
    """
    parser = argparse.ArgumentParser(
        description='Retrieves html file from a livechart link (requires http(s))'
    )
    parser.add_argument('-u', action="store",
                        dest='url',
                        default='https://www.livechart.me/',
                        help='A URL belonging to livechart to retrieve')
    parser.add_argument('-o', action="store",
                        dest='file_name',
                        default='anime.html',
                        help='An output file name')
    return parser.parse_args(args)

def url_check(url):
    """
    Checks if the URL given is valid
    Will raise an exception if there is a feature of the URL missing
    A URL is valid if it contains http(s):// and livechart.me
    :param url: the URL to be checked
    :return: returns nothing
    """
    """
    match = ((url.find('https://www.livechart.me') != -1) or
            (url.find('http://www.livechart.me') != -1) or
            (url.find('https://livechart.me') != -1) or
            (url.find('http://livechart.me') != -1))
    """
    match = ((url.find('http://') != -1 or url.find('https://') != -1) and
            url.find('livechart.me') != -1)
    if not match:
        raise Exception("URL does not belong to livechart.me or missing http(s)")

# Parse arguments
args = parse_args(sys.argv[1:])

# Check if livechart
url_check(args.url)

# Based on: http://stackoverflow.com/questions/13055208/httperror-http-error-403-forbidden
request = urllib.request.Request(args.url, headers=USER_AGENT)
page = urllib.request.urlopen(request)
out = open(args.file_name, "w+")
out.write(page.read().decode('utf-8'))
out.close()
