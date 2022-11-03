# from model import Model
from product import Product

parameters = {
        "Name": "Pañales D1",
        "Description": "Pañales D1",
        "Brand": "D1",
        "Category": "Pañales",
        "CategoryId": "4fd7aa07",
        "Features": 
        {
            "Units": [
            {
                "Name": "30",
                "IsDefault": True
            },
            {
                "Name": "50",
                "IsDefault": False
            }
            ],
            "Sizes": [
            {
                "Name": "Etapa 2",
                "IsDefault": True
            },
            {
                "Name": "Etapa 3",
                "IsDefault": False
            }
            ]
        },
        "SKU": "lksjadfo9",
        "Price": "20000",
        "Discount": {
            "Percentage": 20
        },
        "VirtualStoreId": "VirtualStoreId",
        "VirtualStore": "BabyGift"
    }
ProductModel = Product('babygift-app-MainTableBabyGift', 'PROD')

product = ProductModel.all()
print(product)
# product_cp = product.get_item()
# product_cp['Brand'] = "xxxxxxxxx"
# product.set_item(product_cp)
# product = ProductModel.find('lkjasldf')
# # product.show_varibles()
# print(product)
# # product.show_item()
# print(product.item())
# print(product.save())

# obj_product.show_varibles()

# model = Model('babygift-app-MainTableBabyGift', 'PROD')

# item = model.new(
#     {
#         "Name": "Pañales D1",
#         "Description": "Pañales D1",
#         "Brand": "D1",
#         "Category": "Pañales",
#         "CategoryId": "4fd7aa07",
#         "Features": 
#         {
#             "Units": [
#             {
#                 "Name": "30",
#                 "IsDefault": True
#             },
#             {
#                 "Name": "50",
#                 "IsDefault": False
#             }
#             ],
#             "Sizes": [
#             {
#                 "Name": "Etapa 2",
#                 "IsDefault": True
#             },
#             {
#                 "Name": "Etapa 3",
#                 "IsDefault": False
#             }
#             ]
#         },
#         "SKU": "lksjadfo9",
#         "Price": "20000",
#         "Discount": {
#             "Percentage": 20
#         },
#         "VirtualStoreId": "VirtualStoreId",
#         "VirtualStore": "BabyGift"
#     }
# )

# print(item)
# print(item['Name'])
# item['Name'] = "otro nombre"
# print(item.save())

# # print(model.obj)

# # item.show_item()