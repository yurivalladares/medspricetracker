# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from pytz import timezone
from sqlalchemy.orm import sessionmaker
from medprices.models import Items, create_items_table, db_connect


class MedpricesPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates items table.
        """
        engine = db_connect()
        create_items_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if isinstance(item['price'], str):
            item['price'] = item['price'].replace('R$', '')
            item['price'] = item['price'].replace(' ', '')
            item['price'] = item['price'].replace('.', '')
            item['price'] = item['price'].replace(',', '.')
            item['price'] = float(item['price'])
        if isinstance(item['product_name'], str):
            item['product_name'] = item['product_name'].strip()
        item['scraped_at'] = datetime.now(timezone('America/Sao_Paulo'))
        item['store'] = spider.store

        session = self.Session()
        item = Items(**item)

        try:
            session.add(item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item