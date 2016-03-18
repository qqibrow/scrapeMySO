from __future__ import absolute_import
import random
import scrapy
from scrapy import Request
from mystackoverflow.items import QuestionItem


class MyVotesSpider(scrapy.Spider):
    # This name will be used in command line to run the spider.
    name = "my_votes_spider"
    allowed_domains = ["stackoverflow.com"]
    last_n_page = 1
    cookie = {'acct': 't=Hr4TABitBxsSRea37Ul5JB552qxapuXF&s=KoXekyVpvnqy7Tg10Wwfu5SFw1qASfqf'}

    start_urls = [
        "http://stackoverflow.com/users/1646996/qqibrow?tab=votes&sort=upvote&page=%s" % page for page in
        xrange(1, last_n_page + 1)
        ]

    USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
                   'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
                   ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
                    'Chrome/19.0.1084.46 Safari/536.5'),
                   ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
                    'Safari/536.5'),)

    def start_requests(self):
        for url in self.start_urls:
            request = Request(url, cookies=self.cookie, headers={'User-Agent': random.choice(self.USER_AGENTS)})
            print request.headers
            yield request

    def parse(self, response):
        urls = response.css('.history-table .timeline-answers::attr(href)').extract()
        for url in urls:
            request = Request("http://stackoverflow.com/" + url, callback=lambda r: self.parse_details(r))
            yield request

    def parse_details(self, response):
        item = QuestionItem()
        item['title'] = response.xpath("//div[@id=\"question-header\"]/h1/a/text()").extract()[0]
        item['link'] = response.xpath("//div[@id=\"question-header\"]/h1/a/@href").extract()[0]
        item['tags'] = response.xpath("//div[@class=\"post-taglist\"]/a/text()").extract()
        yield item
