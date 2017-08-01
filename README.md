# JiandanSpider
A simple multiprocessing web spider that can crawl the website Jiandan

## Functions:
 JiandanSpider can crawl and save the information of pics from mezi and wuliao
 session into the database. It will then download the top pictures which has highest likes/unlike/ratio of likes and unlikes to the local
 disk. 

## Key Features:
 * Using multiprocessing to increase the speed
 * Using mongodb and pymongo API to store the initial data

## Built with:
* [Requests](http://www.python-requests.org/en/master/) -Use to handle the HTTP Request 
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) -Use the filter and find the items from website
* [Pymongo](https://api.mongodb.com/python/current/) -Use to manipulate the mongodb database in Python


