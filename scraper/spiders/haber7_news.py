import scrapy
from scrapy import Request
from datetime import datetime

from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule

from news_entry import NewsEntry


class HurriyetNewsSpider(scrapy.Spider):

    name = "haber7_news"
    custom_settings = {
        "ITEM_PIPELINES": {

        },
        "DOWNLOAD_DELAY": 0.01,
    }

    start_urls = ["http://www.haber7.com/"]
    allowed_domains = ['haber7.com']

    def __init__(self, *args, **kwargs):
        super(HurriyetNewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        print(response.url)
        if response.css(".news-content::text").extract_first() is not None:
            yield NewsEntry(
                link = response.url,
                content = ''.join(response.css(".news-content::text, .news-content *::text").extract()),
                title = ''.join(response.css("head h1::text, head h1 *::text").extract()),
                date = ''.join(response.css(".readInfo::text, .readInfo *::text").extract()),
                category = response.url.split('/')[3]
            )
        else:
            for link in LxmlLinkExtractor(allow=self.allowed_domains).extract_links(response):
                if "video" not in link.url:
                    yield Request(link.url, self.parse)
