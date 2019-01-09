import scrapy

class BlogSpider(scrapy.Spider):
    name = 'ConteHistoriasSpider'
    start_urls = ['https://contehistorias.com']

    def parse(self, response):
        categories = response.css('aside.widget_categories ul > li > a::attr(href)').extract()