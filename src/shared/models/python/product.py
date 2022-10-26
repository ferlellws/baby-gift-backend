import uuid
from model import Model
from datetime import datetime

class Product(Model):
    def new(self, item):
        date_time_today = datetime.now()
        date_time_today_str = date_time_today.strftime("%Y-%m-%d %H:%M:%S")

        product = {
            "PK": "product#{}" . format(str(uuid.uuid4().hex)[:8]),
            "SK": 'PRODUCT',
            "Data": "discontinued_1#name_{}" . format(item['Name']),
            "Brand": item['Brand'],
            "Name": item['Name'],
            "Description": item['Description'],
            "CategoryId": item['CategoryId'],
            "Category": item['Category'],
            "Features": item['Features'],
            "Price": item['Price'],
            "SKU": item['SKU'],
            "Discount": item['Discount'],
            "VirtualStoreId": item['VirtualStoreId'],
            "VirtualStore": item['VirtualStore'],
            "CreatedAt": date_time_today_str,
            "UpdatedAt": date_time_today_str
        }

        super().new(product)
        return super()