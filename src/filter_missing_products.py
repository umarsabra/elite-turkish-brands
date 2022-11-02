import csv
from os import path

from config import out_dir, csv_dir



"""
this module search in shopifiy products and find missing products from the extracted products

"""

#get shopifiy products
shopfiy_products_sku = []
with open(path.join(csv_dir, "products_export_2022-10-30.csv"), 'r', encoding='utf8') as shopfiy_products:

    reader = csv.reader(shopfiy_products)
    for products in reader:
        shopfiy_products_sku.append(products[14])



#get extracted products
missing_products = []
with open(path.join(csv_dir, "extracted-products-data-mod.csv"), 'r', encoding='utf8') as extracted_products:

    reader = csv.reader(extracted_products)

    for i, row in enumerate(reader):

        if i == 0:
            missing_products.append(row)

        #skip the title
        else:
            sku = row[1]
            if sku not in shopfiy_products_sku:
                row[2] = row[2].title()
                missing_products.append(row)


#create missing products csc
with open(path.join(out_dir, "missing-products.csv"), 'w', encoding='utf8', newline='') as missing_products_csv:
    writer = csv.writer(missing_products_csv)
    writer.writerows(missing_products)

                
