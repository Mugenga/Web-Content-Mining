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
             if a['href'][:1] == '/' and a['href'][:6] != '/video' :
                if "https://www.nytimes.com" + a['href'] not in article_urls:
                    pass
                    article_urls.append("https://www.nytimes.com" + a['href'])
    urls2 = fetch(main, "").find_all("h2", {"class": "css-qrzo5d e134j7ei0"})
    for url in urls2:
        for a in url:
             if a['href'][:1] == '/' and a['href'][:6] != '/video' :
                if "https://www.nytimes.com" + a['href'] not in article_urls:
                    article_urls.append("https://www.nytimes.com" + a['href'])
    urls3 = fetch(main, "").find_all("h2", {"class": "css-byk1jx"})
    for url in urls3:
        for a in url:
             if a['href'][:1] == '/' and a['href'][:6] != '/video' :
                if "https://www.nytimes.com" + a['href'] not in article_urls:
                    article_urls.append("https://www.nytimes.com" + a['href'])
    return article_urls
    return article_urls


class NytimesspiderSpider(scrapy.Spider):
    name = 'NYTimesSpider'
    allowed_domains = ['nytimes.com']
    
     # Get Politics Artcles 
    politics = getUrls('https://www.nytimes.com/section/politics', "css-1l4spti")
    # Get Business Artcles 
    business = getUrls('https://www.nytimes.com/section/business', "css-1l4spti") 
     # Get Sports Articles
    sports = getUrls('https://www.nytimes.com/section/sports', "css-1l4spti")
    # Arts and Culture Articles can both be found in the entertainment Segment
    arts_cul_cele = getUrls('https://www.nytimes.com/section/arts', "css-1l4spti") 
    
    start_urls = [*politics, *business, *sports, *arts_cul_cele]
    print(start_urls)

    def parse(self, response):
        print("procesing:"+response.url)
        
        title = response.css('.css-rsa88z::text').extract()
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
