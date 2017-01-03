import urllib.request
import shutil

# Consider allowing any livechart page
url = 'https://www.livechart.me/winter-2017/tv'
# Taken from https://www.livechart.me/winter-2017/tv
user_agent = {'User-Agent': 'Mozilla/5.0'}
# file_name = 'test.html'

request = urllib.request.Request(url, headers=user_agent)
page = urllib.request.urlopen(request)
print (page.read().decode('utf-8'))
