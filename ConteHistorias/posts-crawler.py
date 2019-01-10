import scrapy
import datetime

class BlogSpider(scrapy.Spider):
    name = 'ConteHistoriasSpider'
    start_urls = ['https://contehistorias.com']

    def parse(self, response):
        post_urls = response.css('article > header > h2 > a::attr(href)').extract()
        for post_url in post_urls:
            yield scrapy.Request(url = post_url, callback = self.parse_post)            
        
        next_url = response.css('nav.posts-navigation > div.nav-links > div.nav-previous > a::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(url = next_url, callback = self.parse)

    def parse_post(self, response):
        post_title = response.css('h2.entry-title::text').extract_first()
        post_title_parts = post_title.split('|') # pode não haver | no começo
        post_prefix = post_title_parts[0].strip() if len(post_title_parts) > 1 else ''
        post_name = post_title_parts[1].strip() if len(post_title_parts) > 1 else post_title_parts[0].strip()

        url_parts = response.url.split('/')
        publish_year = int(url_parts[3])
        publish_month =int(url_parts[4])
        publish_day = int(url_parts[5])

        yield {
            'title': {
                'original_value': post_title,
                'prefix': post_prefix,
                'name': post_name
            },
            'post_image_url': response.css('article > div.featured-image > span > a > img::attr(data-src)').extract_first(),
            'minutes_to_read': int(response.css('span.wtr-time-number::text').extract_first()),
            'author': response.css('span.author > a::text').extract_first(),
            'publish_date': datetime.date(publish_year, publish_month, publish_day),
            'categories': response.css('span.cat-links > a::text').extract(),
            'tags': response.css('span.tags-links > a::text').extract() 
        }
