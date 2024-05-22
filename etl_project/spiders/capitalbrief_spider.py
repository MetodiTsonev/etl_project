import scrapy
from etl_project.items import ArticleItem

class CapitalBriefSpider(scrapy.Spider):
    name = "capitalbrief_spider"
    start_urls = ['https://www.capitalbrief.com/technology/']

    def parse(self, response):
        articles = response.css('article')
        for article in articles:
            item = ArticleItem()
            item['title'] = article.css('h2 a::text').get()
            article_url = response.urljoin(article.css('h2 a::attr(href)').get())
            item['url'] = article_url
            item['publication_date'] = article.css('time::attr(datetime)').get()
            item['author'] = article.css('a.author::text').get()
            item['images'] = article.css('img::attr(src)').getall()

            request = scrapy.Request(article_url, callback=self.parse_article)
            request.meta['item'] = item
            yield request

        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        item = response.meta['item']
        item['body'] = response.css('#content article p::text').getall()
        yield item