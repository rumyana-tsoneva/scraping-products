import scrapy
import json
from urllib.parse import urljoin, unquote
from ..pipelines import ProductItem

class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://gplay.bg/гейминг-периферия',
        'https://gplay.bg/гейминг-хардуер' 
        ]

    def parse( self, response ):
        
        result = {}
        
        #categories_dropdowns = response.css( 'div.nav-menu' )
        subcategories_links = response.xpath("/html/body/div[@id='vue']/main/div[@class='container pb-4']/div[@class='categories-grid']//div[@class='categories-grid-item']//a//@href").getall()
        # Extract the links (as a list of strings)        
        #links_to_follow = subcategories_links.getall()[4:5] # 38
        # Follow the links to the next parser
        for url in subcategories_links:
            result['category'] = unquote(response.request.url.split("/")[-1])
            result['sub_category'] = url.split("/")[-1].encode("utf-8").decode()
            #next_page = urljoin(self.start_urls[0], url)
            yield response.follow( url = url, callback = self.parse_subcategory ,  meta={'result': result}) #  callback = self.parse_pages


    def parse_subcategory( self, response ):

        result = response.meta['result']
        products =  response.xpath("/html/body/div[@id='vue']/main//div[@class='product-item']//a/@href").getall()[:2]

        for product_url in products:        
            result['product'] = product_url
            yield response.follow( url = product_url, callback = self.parse_product, meta={'result':result})


    def parse_product( self, response ):

        result = response.meta['result']

        product_status = response.xpath("//span[@class='product-status']/@title").get().encode("utf-8").decode()
        product_price = float(response.xpath(".//div[@class='price']//div/price//@*").get()) 
        
        if product_status == 'наличен' and product_price < 200:

            result['title'] = response.xpath("/html//h1/text()").get().encode("utf-8").decode().strip()
            result['subtitle'] = response.xpath("/html/head/title/text()").get().encode("utf-8").decode()
            result['product_number'] = response.xpath("/html//strong/text()").get().strip()
            #result['product_status'] = product_status
            result['price'] = product_price
        
            prod_name = result['product_title']
            filename = f'result_{prod_name}.json'
            with open(filename, 'w') as fp:
                json.dump(result, fp)
