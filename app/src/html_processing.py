from text_processing import *
from ProductData import ProductData
from datetime import datetime


# Returns the text from 1'st level depth of a html tag
def get_plain_text(tag) -> str:
    if tag is None:
        return '-1'
    return  ''.join(x.strip() + ' ' for x in tag.find_all(text=True, recursive=False)).strip()


# Returns an instance of ProductData from a html cars
# Returns None if the card is invalid
def get_data_from_card(html_card, searched_title):
    title = html_card.find('a', class_='product-title js-product-url')

    if not verify_card_title(get_plain_text(title), searched_title):
        return None

    old_price = int(get_plain_text(html_card.find('p', class_='product-old-price').find('s')).replace('.',''))
    new_price = int(get_plain_text(html_card.find('p', class_='product-new-price')).replace('.',''))
    link_to_product = title['href']
    product_id = get_product_id(link_to_product)
    product_data = ProductData(get_plain_text(title), old_price, new_price, product_id, link_to_product, datetime.now())
    return product_data