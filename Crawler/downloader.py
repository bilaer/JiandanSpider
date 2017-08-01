import requests
from urllib.request import urlretrieve
import os

class DownLoader(object):
    def __init__(self):
        pass
    def downloadHTML(self, url):
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r
        else:
            print("error")
            return None

    # P261
    def Schedule(self, blocknum, blocksize, totalsize):
        per = 100 * blocknum * blocksize / totalsize
        if per > 100:
            per = 100

    def downloadPicFromURL(self, url, title, type):
        urlretrieve(url, title+'.'+type, self.Schedule)
