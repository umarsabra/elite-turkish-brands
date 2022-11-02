import csv
import shutil
from os import path
import os
from turtle import title
from config import product_images_dir, selected_products_images_dir, csv_dir, filterd_selected_products, selected_products_resized_images_dir
from helpers import revert_handle



def copy_image(src: str, dist: str):
    with open(path.join(selected_products_resized_images_dir, src), 'rb') as f_src:
        with open(path.join(filterd_selected_products, dist), 'wb') as f_dist:
            shutil.copyfileobj(f_src, f_dist)



products_dict = {}
with open(path.join(csv_dir, "products_export_2022-11-01.csv"), 'r', encoding='utf8') as shopfiy_products:
    reader = csv.reader(shopfiy_products)

    for i, products in enumerate(reader):

        HANDLE = products[0]
        TITLE = products[1]
        SKU = products[14]

        if i != 0 and SKU != "":
            if products_dict.get(HANDLE) == None:
                products_dict.update({
                    HANDLE: [SKU]
                })
            else:
                variants = list(products_dict[HANDLE])
                variants.append(SKU)
                products_dict.update({
                    HANDLE: variants
                })




src_images = os.listdir(selected_products_resized_images_dir)

mod_products_dict = {}
for handle, variants in products_dict.items():
    product_images = []
    for variant in variants:
        

        for image in src_images:


            if image.startswith(variant):
                product_images.append(image)
        
        mod_products_dict.update({
            handle: product_images
        })
        



for handle, variants in mod_products_dict.items():

    dir_title = revert_handle(handle)

    product_folder_path = path.join(filterd_selected_products, dir_title)

    os.mkdir(product_folder_path)

    for image_name in variants:
        copy_image(image_name, path.join(product_folder_path, image_name))


     
        
    

        



            


