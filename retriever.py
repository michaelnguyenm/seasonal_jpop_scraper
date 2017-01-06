import urllib.request
import shutil
import argparse

# Taken from https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
# Required to bypass browser checking on livechart
USER_AGENT = {'User-Agent': 'Mozilla/5.0'}

# Parse arguments
parser = argparse.ArgumentParser(
    description='Retrieves html file from a livechart link'
)
parser.add_argument('-u', action="store",
                    dest='url',
                    default='https://www.livechart.me/',
                    help='A URL belonging to livechart to retrieve')
parser.add_argument('file_name', action="store",
                    help='An output file')
args = parser.parse_args()

# Check if livechart
match = ((args.url.find('https://www.livechart.me') != -1) or
        (args.url.find('http://www.livechart.me') != -1) or
        (args.url.find('https://livechart.me') != -1) or
        (args.url.find('http://livechart.me') != -1))
if not match:
    raise Exception("URL does not belong to livechart.me or missing http(s)")

# Based on: http://stackoverflow.com/questions/13055208/httperror-http-error-403-forbidden
request = urllib.request.Request(args.url, headers=USER_AGENT)
page = urllib.request.urlopen(request)
out = open(args.file_name, "w+")
out.write(page.read().decode('utf-8'))
out.close()
