# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class ProductPipeline(object):

    def open_spider(self, spider):#
        self.conn = sqlite3.connect('products.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS products (ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                                            category CHAR(50) NOT NULL, \
                                            subcategory CHAR(50) NOT NULL, \
                                            title CHAR(100) NOT NULL, \
                                            subtitle CHAR(100) NOT NULL, \
                                            product_number CHAR(100) NOT NULL, \
                                            price INT NOT NULL, \
                                            UNIQUE (category, subcategory, title, subtitle, product_number, price) ON CONFLICT IGNORE)")        

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):

        col = ",".join(item.keys())       
        placeholders = ",".join(len(item) * "?")
        values = list(item.values())
        sql = "INSERT INTO products({}) VALUES({})"
        self.cur.execute(sql.format(col, placeholders), values)

        return item

