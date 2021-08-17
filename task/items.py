# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_jsonschema.item import JsonSchemaItem


class TaskItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
    
    category = scrapy.Field()
    subcategory = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    product_number = scrapy.Field()
    price = scrapy.Field()


class ProductJsonValidator(JsonSchemaItem):
    jsonschema =     {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "Product",
        "description": "A product from GamePlay catalog",
        "type": "object",
        "properties": {
            "id": {
                "description": "The unique identifier for a product",
                "type": "integer"
            },
            "category": {
                "description": "Product main category",
                "type": "string"
            },
            "subcategory": {
                "description": "Product subcategory",
                "type": "string"
            },
            "title": {
                "description": "Name of the product",
                "type": "string"
            },
            "subtitle": {
                "description": "Extended name of the product",
                "type": "string"
            },
            "product_number": {
                "description": "Product number",
                "type": "string"
            },
            "price": {
                "type": "number",
                "minimum": 0,
                "exclusiveMinimum": True
            }
        },
        "required": ["category", "subcategory", "title", "subtitle","product_number", "price"]
    }