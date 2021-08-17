import scrapy
import json
import sqlite3
from urllib.parse import urljoin, unquote
from ..items import ProductItem, ProductJsonValidator
from ..pipelines import ProductPipeline

class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://gplay.bg/гейминг-периферия',
        'https://gplay.bg/гейминг-хардуер' 
        ]

    def parse( self, response ):
        
        item = ProductItem()
        
        subcategories_links = response.xpath("/html/body/div[@id='vue']/main/div[@class='container pb-4']/div[@class='categories-grid']//div[@class='categories-grid-item']//a//@href").getall()
        for url in subcategories_links:
            item['category'] = unquote(response.request.url.split("/")[-1])
            item['subcategory'] = url.split("/")[-1].encode("utf-8").decode()
            yield response.follow( url = url, callback = self.parse_subcategory ,  meta={'item': item}) #  callback = self.parse_pages


    def parse_subcategory( self, response ):

        item = response.meta['item']
        products =  response.xpath("/html/body/div[@id='vue']/main//div[@class='product-item']//a/@href").getall()[:1]

        for product_url in products:        
            yield response.follow( url = product_url, callback = self.parse_product, meta={'item':item})


    def parse_product( self, response ):

        item = response.meta['item']

        product_status = response.xpath("//span[@class='product-status']/@title").get().encode("utf-8").decode()
        product_price = float(response.xpath(".//div[@class='price']//div/price//@*").get()) 
        
        if product_status == 'наличен' and product_price < 200:

            item['title'] = response.xpath("/html//h1/text()").get().encode("utf-8").decode().strip()
            item['subtitle'] = response.xpath("/html/head/title/text()").get().encode("utf-8").decode()
            item['product_number'] = response.xpath("/html//strong/text()").get().strip()
            item['price'] = product_price

        output = ProductJsonValidator(item)

        return output
        
