import scrapy
import bs4 as bs
from urllib.request import Request, urlopen

def fetch(page, addition=''):
    """Fetches HTML data"""
    req = Request(page + addition)
    open_request = urlopen(req).read()
    soup = bs.BeautifulSoup(open_request, 'lxml')
    return soup

def getUrls(main, class_select):
    article_urls = list()
    urls = fetch(main, "").find_all("div", {"class": class_select})
    for url in urls:
        for a in url.find_all("a"):
            if a['href'][:1] == '/':
                if "https://www.newtimes.co.rw" + a['href'] not in article_urls:
                    article_urls.append("https://www.newtimes.co.rw" + a['href'])
    return article_urls


class NewtimesspiderSpider(scrapy.Spider):
    name = 'newtimesspider'
    allowed_domains = ['newtimes.co.rw']
    
    # Get Business Artcles 
    business = getUrls('https://www.newtimes.co.rw/news/business/', "small-push")
    # Get Sports Articles
    sports = getUrls('https://www.newtimes.co.rw/sports/', "x-small-push")
    # Arts and Culture Articles can both be found in the entertainment and Weekender Segment
    arts_cul_cele_1 = getUrls('https://www.newtimes.co.rw/entertainment', "small-push") 
    arts_cul_cele_2 = getUrls("https://www.newtimes.co.rw/weekender", "x-small-push")
    # There is no politics segemnt so I selected the coronavirus segment
    politics = getUrls('https://www.newtimes.co.rw/opinions', "x-small-push")

    joined = [*business, *sports, *arts_cul_cele_1, *arts_cul_cele_2, *politics]
    start_urls = joined

    def parse(self, response):
        print("procesing:"+response.url)
        
        title = response.css('.page-heading::text').extract()
        article = response.css('.article-content > p::text').getall()
        
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
