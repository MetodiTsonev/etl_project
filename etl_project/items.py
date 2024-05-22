import scrapy

class ArticleItem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    publication_date = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
    body = scrapy.Field()