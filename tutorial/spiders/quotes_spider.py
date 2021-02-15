import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa=2',
    ]

    def parse(self, response):
        for quote in response.css('div.box.product'):
            yield {
                'urun': quote.xpath('.//h3/@title').extract_first(),
                'fiyat': quote.xpath('.//del[@class="price old product-old-price"]/text()').get(),
                'indirimli': quote.css("span.price.old.product-old-price::text").get(),
                'SEPETTE': quote.xpath('normalize-space(//div[@class="price-value"])').get(),
                'test': quote.xpath('.//span[@class="price product-price"]/text()').extract_first(),
                'URL': quote.xpath(".//a/@href").get(),
                'ID': quote.xpath('.//a/@data-productid').get(),
                'SKU': quote.xpath('.//a/@data-sku').get(),
            }

