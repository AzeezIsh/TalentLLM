import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = 'Daniyal'
    start_urls = ['https://daniy.al']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from the parsed HTML
        text = soup.get_text(separator='\n', strip=True)
        filename = 'daniyal.txt'
        with open(filename, 'w') as f:
            f.write(text)
        self.log(f'Saved file {filename}')

# Create a crawler process with the spider
process = CrawlerProcess()
process.crawl(MySpider)

# Start the crawling process
process.start()
