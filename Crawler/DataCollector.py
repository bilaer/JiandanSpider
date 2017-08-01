from bs4 import BeautifulSoup
from Crawler.downloader import DownLoader


class DataCollector(object):
    def __init__(self):
        pass

    # Get all the pages of given Jiandan website
    def getAllthePage(self, content, crawl):
        result = set()
        downloader = DownLoader()
        maxPage = self._getCurrentPageNum(content)
        leftURL = ("http://jandan.net/%s/page-" %(crawl))
        rightURL = "#comments"
        for index in range(1, maxPage):
            result.add((leftURL + str(index) + rightURL))

        return result


    # The page number of current page
    def _getCurrentPageNum(self, content):
        soup = BeautifulSoup(content.text, "lxml")
        pageNum = soup.find("div", class_="cp-pagenavi").find("span", class_="current-comment-page")
        result = ""
        for char in pageNum.string:
            if char.isdigit():
                result = result + char
        return int(result)


    # Get the pictures from the page
    def getPicInfoFromPage(self, content):
        result = []
        soup = BeautifulSoup(content.text, "lxml")
        pics = soup.find("ol", class_="commentlist").find_all("li")
        index = 0
        for pic in pics:
            picId = pic.get("id")
            temp = pic.find("div", class_="text")
            # Filter out the ads
            if temp != None:
                picLinks = temp.find("p").find_all("a")
                vote = pic.find("div", class_="jandan-vote")
                like = vote.find("span", class_="tucao-like-container").find("span").string
                unlike = vote.find("span", class_="tucao-unlike-container").find("span").string
                ratio = float(like)/float(unlike)
                picList = []
                for picLink in picLinks:
                    picList.append(picLink.get("href"))
                    result.append({"id": picId,
                                   "picLinks":picList,
                                   "ratio": ratio,
                                   "like": int(like),
                                   "unlike": int(unlike)
                                   })
            index = index + 1
        return result
