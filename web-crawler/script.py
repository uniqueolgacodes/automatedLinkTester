from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.item import Item, Field

class MyItems(Item):
    referer =Field() # where the link is extracted
    response= Field() # url that was requested
    status = Field() # status code received

class MySpider(CrawlSpider):
    name = "test-crawler"
    target_domains = ["dominionuniversity.edu.ng"] # INPUT CRAWLING DOMAIN HERE
    start_urls = ["https://dominionuniversity.edu.ng/"] # THE STARTING URL FOR THE CRAWLER
    handle_httpstatus_list = [404,410,301,500] # If you know backend, it's only 200 by default. you can add more status to list sha

    # This section was added for optimization: I throttle the crawl speed to prevent hitting site too hard
    custom_settings = {
        'CONCURRENT_REQUESTS': 2, # only 2 requests allowed at the same time for optimization (i had to include this line when i noticed a significant reduction in speed)
        'DOWNLOAD_DELAY': 0.5 # delay between requests (this was also added for speed optimiation)
    }

    rules = [
        Rule(
            LinkExtractor( allow_domains=target_domains, deny=('patterToBeExcluded'), unique=('Yes')), 
            callback='parse_my_url', # this method will be called for each request
            follow=True),
        # let the robot crawl the external links but don't follow them
        Rule(
            LinkExtractor( allow=(''),deny=("patterToBeExcluded"),unique=('Yes')),
            callback='parse_my_url',
            follow=False
        )
    ]
#NOTES FOR THE LECTURER
# 1. The crawler will crawl the links in the start_urls list and the links that are extracted from the start_urls
# The first rule says: extract all unique links under the target_domains and follow them, but exclude those who contains patterToBeExcluded.
# The second rule says: extract all unique links but do not follow them and exclude those who contains patterToBeExcluded.


    def parse_my_url(self, response):
      # In here, we need to have the list of response codes that we want to include on the report, we know that 404
      report_if = [404] 
      if response.status in report_if: # if the response matches, then creates a MyItem
          item = MyItems()
          item['referer'] = response.request.headers.get('Referer', None)
          item['status'] = response.status
          item['response']= response.url
          yield item
      yield None # if the response did not match return an empty report

    
#run with scrapy runspider script.py -o report-file.csv