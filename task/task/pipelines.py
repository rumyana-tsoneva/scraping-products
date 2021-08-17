# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy_jsonschema.item import JsonSchemaItem

class TaskPipeline:
    def process_item(self, item, spider):
        return item


class ProductItem(JsonSchemaItem):
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
                "description": "Name of the product",
                "type": "string"
            },
            "subcategory": {
                "description": "Name of the product",
                "type": "string"
            },
            "title": {
                "description": "Name of the product",
                "type": "string"
            },
            "subtitle": {
                "description": "Name of the product",
                "type": "string"
            },
            "product_number": {
                "description": "Name of the product",
                "type": "string"
            },
            "price": {
                "type": "number",
                "minimum": 0,
                "exclusiveMinimum": True
            }
        },
        "required": ["id", "category", "subcategory", "title", "subtitle","product_number", "price"]
    }

