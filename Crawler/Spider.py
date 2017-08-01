from Crawler.DataCollector import DataCollector
from Crawler.downloader import DownLoader
from Crawler.DataManager import DataManager
from multiprocessing import Pool, cpu_count, Manager
import time, os


class Spider(object):
    def __init__(self):
        self.meiziLink = "http://jandan.net/ooxx"
        self.wuliaoLink = "http://jandan.net/pic"
        self.jiandanDir = "Jiandan"
        self.meiziDir = "Jiandan/Pic/meiziPic"
        self.wuliaoDir = "Jiandan/Pic/wuliaoDir"
        self.dbName = "Jiandan"
        self.wuliaoColName = "wuliaoPic"
        self.meiziColName = "meiziPic"
        self.MeiziPageList = set()
        self.WuliaoPageList = set()
        self.collector = DataCollector()
        self.downloader = DownLoader()
        self.initSpider()


    def runSpider(self, **crawl):
        print("Creating dir for pics")
        self.initSpider()

        # Get the data of meizi session
        self.getLinkOfAllPic("Meizi")
        print("Get the top picture...")
        self.getTopNPic(20, "Meizi")

        # Get the data of wuliao session
        self.getLinkOfAllPic("Wuliao")
        print("Get the top picture...")
        self.getTopNPic(20, "Wuliao")


    # Initialize the spider including the directories as well as sites content
    # as start
    def initSpider(self):
        self.initDir()

        urlContent = self.downloader.downloadHTML(self.meiziLink)
        self.MeiziPageList = self.collector.getAllthePage(urlContent, "ooxx")

        urlContent = self.downloader.downloadHTML(self.wuliaoLink)
        self.WuliaoPageList = self.collector.getAllthePage(urlContent, "pic")


    # Initialize the directories for storing the data
    def initDir(self):
        if not os.path.isdir(self.jiandanDir):
            os.makedirs(self.meiziDir)
            os.makedirs(self.wuliaoDir)
        else:
            return

    # Get all the links of pictures from all the pages collected
    # and save them to the database
    def getLinkOfAllPic(self, crawl):
        print("Initialize pool")
        lock = Manager().Lock()
        if crawl == "Meizi":
            print("Created a pool for meizi picture collecting")
            pool = Pool(cpu_count())
            for page in self.MeiziPageList:
                pool.apply_async(self._getPic, args=(page, crawl, self.collector, self.downloader, lock))
            pool.close()
            pool.join()
            print("Collection finished")
        elif crawl == "Wuliao":
            print("Created a pool for wuliao picture collecting")
            pool = Pool(cpu_count())
            for page in self.WuliaoPageList:
                pool.apply_async(self._getPic, args=(page, crawl, self.collector, self.downloader, lock))
            pool.close()
            pool.join()
            print("Collection finished")

        else:
            exit(1)


    def _getPic(self, page, crawl, collector, downloader, lock):
        print("Child process %s collecting pic" %os.getpid())
        print("Collecting page: %s" %page)
        if crawl == "Wuliao":
            manager = DataManager(self.dbName, self.wuliaoColName)
        elif crawl == "Meizi":
            manager = DataManager(self.dbName, self.meiziColName)
        else:
            print("wrong request")
            return

        pageContent = downloader.downloadHTML(page)
        time.sleep(2)
        # Get all the links of pictures from the site
        info = collector.getPicInfoFromPage(pageContent)
        time.sleep(2)
        print("Save to the data base...")
        lock.acquire()
        # Save the data to the mongodb database
        for pic in info:
            manager.saveDataToDB(pic)
        lock.release()
        print("Finished Saving")
        print("Child process %s finish collection" %os.getpid())

    def getTopNPic(self, num, crawl):

        if crawl == "Meizi":
            manager = DataManager(self.dbName, self.meiziColName)
            dir = self.meiziDir
        elif crawl == "Wuliao":
            manager = DataManager(self.dbName, self.wuliaoColName)
            dir = self.wuliaoDir
        else:
            print("Wrong type")
            return

        # Get the top pictures with most likes
        topPic = manager.sortDBbyKey("like", num)

        # Store the top pics into the disk
        for pics in topPic:
            if not os.path.isdir(dir + "/" + pics["id"]):
                os.mkdir(dir + "/" + pics["id"])
            index = 0
            print("Start download %s" % pics["id"])
            for pic in pics["picLinks"]:
                # Correct the format of url
                pic = "http:" + pic
                # Get the type of pic
                picType = self._getPicType(pic)
                # Set up the title of pic
                title = dir + "/" + pics["id"] + "/" + str(index)
                self.downloader.downloadPicFromURL(pic, title, picType)
                index = index + 1
        print("Pics have been downloaded")


    def _getPicType(self, url):
        index = len(url) - 1
        type = ""
        while url[index] != ".":
            type = url[index] + type
            index = index - 1
        return type



if __name__ == "__main__":
    test = Spider()
    test.runSpider()

