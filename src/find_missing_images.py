import os
from config import selected_products_images_dir, selected_products_resized_images_dir


resized_images = os.listdir(selected_products_resized_images_dir)
resized_images_ex = []

stock_images = os.listdir(selected_products_images_dir)
stock_images_ex = []






for stock in stock_images:
    stock_images_ex.append(stock.split('.')[0])

for resized in resized_images:
    resized_images_ex.append(resized.split('.')[0])

missing_images = []
for image in stock_images_ex:
    if image in resized_images_ex:
        missing_images.append(image)


print(len(missing_images))