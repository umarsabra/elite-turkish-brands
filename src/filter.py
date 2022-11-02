import csv
import os
from config import csv_dir, product_images_dir, out_dir


"""
This module adds to the extracted data from the images the color and the image count existed 
for each product accourding to the sku it has

"""

#In
in_product_data_csv = "missing-products-with-mod-title.csv"
out_product_data_csv_with_image_color = "missing-product-with-image-color.csv"

        
#Getting all products images SKU from images folder
drive_images = []
for image in os.listdir(product_images_dir):
    image_without_extention = image.split(".")[0]
    drive_images.append(image_without_extention)
 


#Loading selected products SKU
sku = []
with open(os.path.join(csv_dir, in_product_data_csv), "r", encoding="utf8") as product_data:
    reader = csv.reader(product_data)
    for image_name in reader:
        sku.append(image_name[1])

          

found = []
not_found = []          
sku_image_count = {"SKU": 0}
for selected_product in sku:
    if selected_product in drive_images:
        found.append(selected_product)
        image_count = 0
        # Finding product multible photos
        for product_image in drive_images:
            if product_image.startswith(selected_product) or product_image == drive_images:
                image_count += 1
                sku_image_count.update({selected_product: image_count})
    else:
        sku_image_count.update({selected_product: 0})
        not_found.append(selected_product)
            



#Create CSV with image count and color
with open(os.path.join(out_dir, out_product_data_csv_with_image_color), "w", encoding="utf8", newline='') as final_csv:
    writer = csv.writer(final_csv)
    rows = []
    with open(os.path.join(csv_dir, in_product_data_csv), "r", encoding="utf8") as data:
        reader = csv.reader(data)
        for i, row in enumerate(reader):

            #Means the row title
            if i == 0:

                #Adding IMAGE COUNT and COLOR COLUMNS to the title
                title_row = [*row, "IMAGE COUNT", "COLOR"]
                rows.append(title_row)

            else:

                #Fix title capitalization
                row[2] = str(row[2]).title()

                #Get the last two digets from the SKU to identify the color
                sku_last_digit = str(row[1]).split("-")[-1]

                #18 = GOLD
                if sku_last_digit == "18":
                    new_row = [*row, sku_image_count[row[1]], "Gold"]
                    rows.append(new_row)

                #11 OR 19 = SILVER
                elif sku_last_digit == "11" or sku_last_digit == "19":
                    new_row = [*row, sku_image_count[row[1]], "Silver"]
                    rows.append(new_row)

                #COLOR IS NOT DEFINED
                else:
                    new_row = [*row, sku_image_count[row[1]], "UNDEFINED"]
                    rows.append(new_row)

    #Write the rows from the modified rows array
    writer.writerows(rows)


not_found.pop(0)
for item in not_found:
    print(item)
print(len(not_found))