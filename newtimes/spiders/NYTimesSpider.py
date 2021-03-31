import scrapy
import bs4 as bs
from urllib.request import Request, urlopen

def fetch(page, addition=''):
    """Fetches HTML data"""
    req = Request(page + addition)
    open_request = urlopen(req).read()
    soup = bs.BeautifulSoup(open_request, 'lxml')
    return soup


def getUrls(main, selector_class):
    article_urls = list()
    urls = fetch(main, "").find_all("div", {"class": selector_class})
    for url in urls:
        for a in url:
             if a['href'][:1] == '/':
                if "https://www.nytimes.com" + a['href'] not in article_urls:
                    article_urls.append("https://www.nytimes.com" + a['href'])
    return article_urls


class NytimesspiderSpider(scrapy.Spider):
    name = 'NYTimesSpider'
    allowed_domains = ['nytimes.com']
    
     # Get Politics Artcles 
    politics = getUrls('https://www.nytimes.com/section/politics', "css-1l4spti")
    # Get Business Artcles 
    #business = getUrls('https://www.washingtonpost.com/business', "headline")
     # Get Sports Articles
    #sports = getUrls('https://www.washingtonpost.com/sports', "headline")
    # Arts and Culture Articles can both be found in the entertainment Segment
    #arts_cul_cele = getUrls('https://www.washingtonpost.com/entertainment', "") 
    
    start_urls = [*politics]

    def parse(self, response):
        print("procesing:"+response.url)
        
        title = response.css('#link-ef6af63::text').extract()
        article = response.css('.css-1fanzo5 > div > p::text').getall()
        
        row_data=zip(title, str(article))
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                #key:value
                'page':response.url,
                'title' : item[0],
                'article' : article,
            }

        #yield or give the scraped info to scrapy
        yield scraped_info
