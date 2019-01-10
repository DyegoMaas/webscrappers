import scrapy

class BlogSpider(scrapy.Spider):
    name = 'ConteHistoriasSpider'
    start_urls = ['https://contehistorias.com']

    def parse(self, response):
        post_urls = response.css('article > header > h2 > a::attr(href)').extract()
        for post_url in post_urls:
            yield scrapy.Request(url = post_url, callback = parse_post)            
        
        next_url = response.css('nav.posts-navigation > div.nav-links > div.nav-previous > a::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(url = next_url, callback = self.parse)

    def parse_post(self, response):
        yield 'x' # TODO parse post :)