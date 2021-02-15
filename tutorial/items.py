# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
 
    #product related items
    gender=Field()
    productId=Field()
    productName=Field()
    priceOriginal=Field()
    priceSale=Field()
    badge=Field()

    #items to store links 
    imageLink = Field()
    productLink=Field()

    #item for company name
    company = Field()

    #items for image pipeline
    #image_urls = scrapy.Field()
    #images = scrapy.Field()
    pass

class ImgData(Item):
    image_urls=scrapy.Field()
    images=scrapy.Field()