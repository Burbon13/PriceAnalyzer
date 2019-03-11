from bs4 import BeautifulSoup
from Domain import ProductData
from datetime import datetime
from text_processing import verify_card_title, get_product_id


# Returns the text from 1'st level depth of a html tag
def get_plain_text(tag) -> str:
    if tag is None:
        return '-1'
    return  ''.join(x.strip() + ' ' for x in tag.find_all(text=True, recursive=False)).strip()


# Will return a history instance from a certain products page
def get_history_from_product_page(html_page, shop='emag'):
    fun_dict = {'emag': ghfpp_emag}
    return fun_dict[shop](html_page)


def ghfpp_emag(html_page):
    print(html_page)
    return 'haah'


def scan_html_for_products(html_data, shop, product_name):
    html_soup = BeautifulSoup(html_data, 'html.parser')
    if shop == 'emag':
        return scan_emag_html(html_soup, product_name)
    return None

# Returns a ProductData list from an html emag search page
def scan_emag_html(html_soup, product_name):
    product_data_list = []
    for html_card in html_soup.find_all('div', class_='card-item js-product-data'):
            data = get_data_from_card(html_card, product_name)
            if data:
                product_data_list.append(data)
    return product_data_list


# Returns an instance of ProductData from a html
# Returns None if the card is invalid
def get_data_from_card(html_card, searched_title, shop='emag'):
    fun_dict = {'emag': gdfc_emag}
    return fun_dict[shop](html_card, searched_title)


def gdfc_emag(html_card, searched_title):
    title = html_card.find('a', class_='product-title js-product-url')

    if not verify_card_title(get_plain_text(title), searched_title):
        return None

    old_price = int(get_plain_text(html_card.find('p', class_='product-old-price').find('s')).replace('.',''))
    new_price = int(get_plain_text(html_card.find('p', class_='product-new-price')).replace('.',''))
    link_to_product = title['href']
    product_id = get_product_id(link_to_product)
    product_data = ProductData(get_plain_text(title), old_price, new_price, product_id, link_to_product, datetime.now())
    return product_data