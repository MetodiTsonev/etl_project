import scrapy
from etl_project.items import ArticleItem

class RestOfWorldSpider(scrapy.Spider):
    name = "restofworld_spider"
    start_urls = ['https://restofworld.org/series/the-rise-of-ai/']

    def parse(self, response):
        for article in response.css('article'):
            item = ArticleItem()
            item['title'] = article.css('h2.headline::text').get()
            article_url = response.urljoin(article.css('a::attr(href)').get())
            item['url'] = article_url
            item['publication_date'] = article.css('time::attr(datetime)').get()
            item['author'] = article.css('a.author.url.fn::text').get()
            item['images'] = article.css('img::attr(src)').getall()

            request = scrapy.Request(article_url, callback=self.parse_article)
            request.meta['item'] = item
            yield request

        next_page = response.css('div.nav-previous a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        item = response.meta['item']
        item['body'] = response.css('div.post-content p::text').getall()
        yield item