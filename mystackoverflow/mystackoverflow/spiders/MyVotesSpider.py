import scrapy
from scrapy import Request


class MyVotesSpider(scrapy.Spider):
    name = "my_votes_spider"
    allowed_domains = ["stackoverflow.com"]
    last_n_page = 1
    cookie = {'acct': 't=nQROneS%2bxGGnVJnlLzBpiet0KVO0Qhsn&s=eHNqjvONlOG1FA5iY8iy0OWxnhB7pV4V'}

    start_urls = [
        "http://stackoverflow.com/users/1646996/qqibrow?tab=votes&sort=upvote&page=%s" % page for page in
        xrange(1, last_n_page + 1)
        ]

    def start_requests(self):
        for url in self.start_urls:
            request = Request(url, cookies=self.cookie)
            print request.headers
            yield request

    def parse(self, response):
        urls = response.css('.history-table .timeline-answers::attr(href)').extract()
        for url in urls:
            request = Request("http://stackoverflow.com/" + url, callback=lambda r: self.parse_details(r))
            yield request

    def parse_details(self, response):
        yield {
            "url": response.url
        }
