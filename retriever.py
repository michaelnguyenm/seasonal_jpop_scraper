import urllib.request
import shutil

# Based on: http://stackoverflow.com/questions/13055208/httperror-http-error-403-forbidden
#
# Consider allowing any livechart page
url = 'https://www.livechart.me/winter-2017/tv'
# Taken from https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
user_agent = {'User-Agent': 'Mozilla/5.0'}
# file_name = 'test.html'

request = urllib.request.Request(url, headers=user_agent)
page = urllib.request.urlopen(request)
print (page.read().decode('utf-8'))
