import uuid
from model import Model
from datetime import datetime

LABEL_PRODUCT = 'CATEGORY'
class Category(Model):
    SK = LABEL_PRODUCT

    def new(self, item):
        date_time_today = datetime.now()
        date_time_today_str = date_time_today.strftime("%Y-%m-%d %H:%M:%S")
        category_id = str(uuid.uuid4().hex)[:8]

        if item['ParentsId'] != '':
            parents_id = '#' + item['ParentsId']

        product = {
            "PK": "category#{}" . format(category_id),
            "SK": self.SK,
            "Data": f"""{item['Name']}{parents_id}#{category_id}""",
            "Name": item['Name'],
            "Description": item['Description'],
            "Active": True,
            "CreatedAt": date_time_today_str,
            "UpdatedAt": date_time_today_str
        }

        super().new(product)
        return super()


    def create(self, item):
        return super().create(item)


    def find(self, id):
        return super().find(LABEL_PRODUCT.lower() + "#" + id + "_" + LABEL_PRODUCT)


    def all(self, sk=LABEL_PRODUCT):
        return super().all(sk)

