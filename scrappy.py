import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = 'Daniyal'
    start_urls = ['https://daniy.al']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        text = soup.get_text(separator='\n', strip=True)
        filename = 'daniyal.txt'
        with open(filename, 'w') as f:
            f.write(text)
        self.log(f'Saved file {filename}')


process = CrawlerProcess()
process.crawl(MySpider)


process.start()
