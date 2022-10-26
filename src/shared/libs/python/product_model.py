import uuid
import json
from base_models import Model
from datetime import datetime

class Product:
    def __init__(self, item):
        date_time_today = datetime.now()
        date_time_today_str = date_time_today.strftime("%Y-%m-%d %H:%M:%S")
        self.data = "discontinued_1#name_{}" . format(item['Name'])
        self.pk = "product#{}" . format(str(uuid.uuid4().hex)[:8])
        self.sk = 'PRODUCT'
        self.name = item['Name']
        self.brand = item['Brand']
        self.description = item['Description']
        self.category_id = item['CategoryId']
        self.category = item['Category']
        self.features = item['Features']
        self.price = item['Price']
        self.sku = item['SKU']
        self.discount = item['Discount']
        self.virtual_store_id = item['VirtualStoreId']
        self.virtual_store = item['VirtualStore']
        self.created_at = date_time_today_str
        self.updated_at = date_time_today_str


    def to_item(self):
        product = {
            "Data": self.data,
            "Brand": self.brand,
            "Name": self.name,
            "Description": self.description,
            "CategoryId": self.category_id,
            "Category": self.category,
            "Features": self.features,
            "Price": self.price,
            "SKU": self.sku,
            "Discount": self.discount,
            "VirtualStoreId": self.virtual_store_id,
            "VirtualStore": self.virtual_store,
            "CreatedAt": self.created_at,
            "UpdatedAt": self.updated_at
        }

        keys = Model(self.pk, self.sk).get_keys()
        return {**keys, **product}


    def show_item(self):
        print(self.to_item())