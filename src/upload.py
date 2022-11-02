import csv
import json
from math import ceil
import os


from helpers import create_handel, generate_random_price
from config import out_dir, templates_dir


"""
this module creates a csv file to import in shopify products it takes a file format with the following colums 
CODE 2,SKU,TITLE,QUANTITY,PACKAGE WEIGHT,PACKAGE WIDTH,PACKAGE LENGTH,PACKAGE HIGHT,ITEM WEIGHT,IMAGE COUNT,COLOR

"""





in_csv = "missing-product-with-image-color.csv"
out_csv = "final-shopify-missing-products.csv"

#Read csv
products_dict = {}
with open(os.path.join(out_dir, in_csv), 'r', encoding='utf8') as products_data:
    reader = csv.reader(products_data)
    for i, products in enumerate(reader):

        #NOT THE TABLE TITILE
        if i != 0:

            #if product is not added already to the dict

            if products_dict.get(products[2]) == None:
                products_dict.update({ products[2]: {
                    'CODE 2': products[0],
                    'SKU': products[1],
                    'TITLE': products[2],
                    'QUANTITY': products[3],
                    'PACKAGE WEIGHT': products[4],
                    'PACKAGE WIDTH': products[5],
                    'PACKAGE LENGTH': products[6],
                    'PACKAGE HIGHT': products[7],
                    'ITEM WEIGHT': products[8],
                    'COLOR': products[10],
                    'VARIANTS': []
                }})

            #Product is added to the dict
            else:

                #check if the main product color is silver and change it to gold and change the product SKU
                if products_dict[products[2]]['COLOR'] == 'Silver':

                    product_dict = dict(products_dict[products[2]])
                    current_variants = list(product_dict['VARIANTS'])

                    current_variants.append({
                            'CODE 2': products_dict[products[2]]['CODE 2'],
                            'SKU': products_dict[products[2]]['SKU'],
                            'COLOR': products_dict[products[2]]['COLOR'],
                        })

                    product_dict.update({
                        'VARIANTS': current_variants
                    })


                    product_dict.update({
                        'COLOR': 'Gold',
                        'CODE 2': products[0],
                        'SKU': products[1]
                    })

                    #commit the changes
                    products_dict.update({products[2]: product_dict})

                #add a variant to the existing product
                elif products_dict[products[2]]['COLOR'] == 'Gold':


                    product_dict = dict(products_dict[products[2]])

                    current_variants = list(product_dict['VARIANTS'])

                    current_variants.append({
                        'COLOR': products[10],
                        'CODE 2': products[0],
                        'SKU': products[1]
                        })

                    #update variants
                    product_dict.update({
                        'VARIANTS': current_variants
                    })

                    #commit the changes
                    products_dict.update({products[2]: product_dict})



shopifiy_records = []
default_dict = {}
with open(os.path.join(templates_dir, "temp_default.json"), 'r', newline='') as shopifiy_temp:

    default_dict = dict(json.load(shopifiy_temp))
    
    
    for item in products_dict.keys():
        
        #Check if product has variants
        if len(products_dict[item]['VARIANTS']) > 0:

            record = default_dict.copy()

            handle = create_handel(item)
            price = generate_random_price()
            weight_in_grams = ceil(float(products_dict[item]['PACKAGE WEIGHT']) * 1000)
            quantity = products_dict[item]['QUANTITY']



            record.update(
                {
                    'Vendor': 'Elite Turkish Brands',
                    'Published': 'TRUE',
                    'Option1 Name': 'Color',
                    'Gift Card': 'FALSE',
                    'Title': item,

                    'Handle': handle,
                    'Option1 Value': products_dict[item]['COLOR'],
                    'Variant SKU': products_dict[item]['SKU'],
                    'Variant Grams': weight_in_grams,
                    'Variant Inventory Qty': quantity,
                    'Variant Price': price,
                    'Variant Barcode': products_dict[item]['CODE 2']

                }
            )

            #Commit
            shopifiy_records.append(record)

            variants = list(products_dict[item]['VARIANTS'])

            for variant in variants:
                variant_record = default_dict.copy()

                variant_record.update(
                    {

                    'Handle': handle,
                    'Option1 Value': variant['COLOR'],
                    'Variant SKU': variant['SKU'],
                    'Variant Grams': weight_in_grams,
                    'Variant Inventory Qty': quantity,
                    'Variant Price': price,
                    'Variant Barcode': variant['CODE 2']

                }
                )

                #Commit
                shopifiy_records.append(variant_record)
        elif len(products_dict[item]['VARIANTS']) == 0:
            record = default_dict.copy()

            handle = create_handel(item)
            price = generate_random_price()
            weight_in_grams = ceil(float(products_dict[item]['PACKAGE WEIGHT']) * 1000)
            quantity = products_dict[item]['QUANTITY']



            record.update(
                {
                    'Vendor': 'Elite Turkish Brands',
                    'Published': 'TRUE',
                    'Option1 Name': 'Color',
                    'Gift Card': 'FALSE',
                    'Title': item,
                    'Handle': handle,
                    'Option1 Value': products_dict[item]['COLOR'],
                    'Variant SKU': products_dict[item]['SKU'],
                    'Variant Grams': weight_in_grams,
                    'Variant Inventory Qty': quantity,
                    'Variant Price': price,
                    'Variant Barcode': products_dict[item]['CODE 2']

                }
            )

            #Commit
            shopifiy_records.append(record)
           


#Create final output
with open(os.path.join(out_dir, out_csv), 'w', encoding='utf8', newline='') as shofiy_products:

    writer = csv.writer(shofiy_products)

    title_row = default_dict.keys()
    writer.writerow(title_row)

    for records in shopifiy_records:
        record_dict = dict(records)
        writer.writerow(record_dict.values())

    
        
