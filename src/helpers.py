import random



def generate_random_price():
    price = random.uniform(8.0, 30.0)
    return round(price, 2) 

def revert_handle(handle: str):
    return handle.replace("-", " ").title()


def create_handel(title: str):
    return title.strip().lower().replace(' ', '-')


def get_product_type(title: str):

    product_type = ""

    product_title = title.lower()


    title_words = product_title.split()

    if "tea" in title_words and "set" in title_words:
        product_type = "tea_set"

    elif "coffee" in title_words and "set" in title_words:
        product_type = "coffee_set"

    elif "presentation" in title_words and "set" in title_words:
        product_type = "presentation_set"

    else:
        product_type = "generic"

    # if tea_position > 0:
    #     product_type = "tea_set"
    # elif coffee_position > 0:
    #     product_type = "coffee_set"
    # else:
    #      product_type = None

    return product_type