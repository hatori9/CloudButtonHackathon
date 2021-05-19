import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
import json
from lithops import Storage
from analyseHtml import getText
bucket='cloudbuttonhackathon'                  #Change this value if you want to change the storage bucket

class TestSpider(scrapy.Spider):
  name = "test" 


  def parse(self, response):
    urls_all = []    # Used to collect all the links first.
    urls_follow = [] # Links to finally follow/crawl
    # Find and extract all links into the list.
    for link in response.css('a::attr(href)').extract():
      url = response.urljoin(link)
      urls_all.append(url)

    # Analyze and remove unwanted links
    # Assuming we wish to ignore/drop urls odd-number indexed links
    # Add only even number indexed links to urls_follow 
    for i in range( len( urls_all ) ):
      if i % 2 == 0:
        urls_follow.append( urls_all[i] )

    # Finally let's create and yield all the requests to even numbered index links
    for link_to_follow in urls_follow:
      yield scrapy.Request(link_to_follow, callback=self.processEvenNumberedLink)
      
  def processEvenNumberedLink(self, response):
    # Do something useful/meaningful.
    self.logger.info("Following %s", response.url) 
    page = response.url.split("/")[-2]
    filename = f'{page}.html'
    #with open(filename, 'wb') as f:
    #   f.write(response.body)
    storage = Storage()
    print(filename)
    storage.put_object(bucket,filename,getText(response.body))

process = CrawlerProcess()


def getWebsHtml(link):
    #TestSpider.start_urls=['https://www.reddit.com/r/COVID19/']     #Example
    TestSpider.start_urls=[link]
    process.crawl(TestSpider)
    process.start() # the script will block here until the crawling is finished
    storage = Storage()
    list=storage.list_keys(bucket)
    filenames=[]
    texts=[]
    for a in list:
      filenames.append(a)
      text=storage.get_object(bucket,a)
      texts.append(str(text))
    dict={
      "filenames":filenames,
      "texts":texts,
        }

    list=storage.list_keys('cloudbuttonhackathon')
    storage.delete_objects('cloudbuttonhackathon',list)

    storage.put_object(bucket,"dataWEB.json",json.dumps(dict))



