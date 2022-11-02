
import csv
import os


from helpers import get_product_type
from config import csv_dir, templates_dir, out_dir

"""

This module analyzed the product title and identify the follows
1- if it was a coffee or a tea set
2- if yes for how many people
3- creates the description the product description

"""


#read coffee set temp
coffee_set_html = ""
with open(os.path.join(templates_dir, "coffee_set.html"), 'r') as coffee_set_temp:
    coffee_set_html = "".join(coffee_set_temp.readlines())

#read tea set temp
tea_set_html = ""
with open(os.path.join(templates_dir, "tea_set.html"), 'r') as tea_set_temp:
    tea_set_html = "".join(tea_set_temp.readlines())
    



#processing...
products_with_description = []
with open(os.path.join(csv_dir, "products_export_without_description.csv"), 'r', encoding='utf8', newline='') as products:
    reader = csv.reader(products)

    for i, product in enumerate(reader):

        title = product[1]
        body = product[2]

        #pass the table title and empty title
        if i !=0 and title != "":

            product_type = get_product_type(title)

            if product_type == "coffee_set":
                product[2] = coffee_set_html
                products_with_description.append(product)

                
            elif product_type == "tea_set":
                product[2] = tea_set_html
                products_with_description.append(product)


            else:
                products_with_description.append(product)
        else:
            products_with_description.append(product)


            
with open(os.path.join(out_dir, "products_with_description.csv"), 'w', encoding='utf8', newline='') as output:
    writer = csv.writer(output)
    writer.writerows(products_with_description)
       
        
        
    

