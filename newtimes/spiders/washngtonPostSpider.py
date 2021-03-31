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
    urls = fetch(main, "").find_all("h2", {"class": selector_class})
    for url in urls:
        for a in url:
            article_urls.append(a['href'])
    return article_urls


class WashngtonpostspiderSpider(scrapy.Spider):
    name = 'washngtonPostSpider'
    allowed_domains = ['washingtonpost.com']
    
    # Get Politics Artcles 
    politics = getUrls('https://www.washingtonpost.com/politics', "")
    # Get Business Artcles 
    business = getUrls('https://www.washingtonpost.com/business', "headline")
     # Get Sports Articles
    sports = getUrls('https://www.washingtonpost.com/sports', "headline")
    # Arts and Culture Articles can both be found in the entertainment Segment
    arts_cul_cele = getUrls('https://www.washingtonpost.com/entertainment', "") 
    
    start_urls = [*politics, *business, *sports, *arts_cul_cele]
    
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):

        print("procesing:"+response.url)
        
        title = response.css('#main-content > span::text').extract()
        article = response.css('.article-body > div > section > div > p::text').getall()
        
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

