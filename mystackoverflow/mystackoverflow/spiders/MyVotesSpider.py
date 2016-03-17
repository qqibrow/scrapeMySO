import scrapy
from scrapy import Request


class MyVotesSpider(scrapy.Spider):
    name = "my_votes_spider"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/users/1646996/qqibrow?tab=votes"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          cookies={'acct': 't=lahjjX631H03FxvqKwT9GcXk601MFM4N&s=nL3yDBKOyNMOhIUNa2kg9plM9jFu%2blgy'})

    def parse(self, response):
        yield {
            'link': response.css('.history-table .timeline-answers::attr(href)').extract()
        }
