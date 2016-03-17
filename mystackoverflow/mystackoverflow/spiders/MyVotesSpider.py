import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request


class MyVotesSpider(CrawlSpider):
    name = "my_votes_spider"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/users/1646996/qqibrow?tab=votes"
    ]

    rules = [
        Rule(LinkExtractor(allow=('stackoverflow.com/users/1646996/qqibrow?tab=votes')), follow=False, callback='parse_item')
    ]

    def start_requests(self):
        for url in self.start_urls:
            print url
            yield Request(url,
                          cookies={'acct': 't=lahjjX631H03FxvqKwT9GcXk601MFM4N&s=nL3yDBKOyNMOhIUNa2kg9plM9jFu%2blgy'})

    def parse_item(self, response):
        yield {
            'url': response.url
        }

