from scrapy.item import Item, Field


class NewsEntry(Item):
    link = Field()
    date = Field()
    title = Field()
    content = Field()
    category = Field()