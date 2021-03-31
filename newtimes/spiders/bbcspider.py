import scrapy
import bs4 as bs
from urllib.request import Request, urlopen

def fetch(page, addition=''):
    """Fetches HTML data"""
    req = Request(page + addition)
    open_request = urlopen(req).read()
    soup = bs.BeautifulSoup(open_request, 'lxml')
    return soup


def getUrls(main):
    article_urls = list()
    urls = fetch(main, "").find_all("div", {"class": "gel-1/2@xs"})
    for url in urls:
        for a in url.find_all("a"):
            if a['href'][:1] == '/':
                if "https://www.bbc.com" + a['href'] not in article_urls:
                    article_urls.append("https://www.bbc.com" + a['href'])
    urls2 = fetch(main, "").find_all("div", {"class": "gel-5/8@l"})
    for url in urls2:
        for a in url.find_all("a"):
            if a['href'][:1] == '/':
                if "https://www.bbc.com" + a['href'] not in article_urls:
                    article_urls.append("https://www.bbc.com" + a['href'])
    return article_urls


class BbcspiderSpider(scrapy.Spider):
    name = 'bbcspider'
    allowed_domains = ['bbc.com']
    
    # Get Politics Artcles 
    politics = getUrls('https://www.bbc.com/news/politics')
      # Get Business Artcles 
    business = getUrls('https://www.bbc.com/news/business')
    # Get Sports Articles
    sports = getUrls('https://www.bbc.com/sport')
    # Arts and Culture Articles can both be found in the entertainment Segment
    arts_cul_cele = getUrls('https://www.bbc.com/news/entertainment_and_arts') 
    
    start_urls = joined = [*politics, *business, *sports, *arts_cul_cele]

    def parse(self, response):
        print("procesing:"+response.url)
        
        title = response.css('#main-heading::text').extract()
        article = response.css('.e5tfeyi2 > p::text').getall()
        
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
