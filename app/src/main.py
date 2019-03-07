import requests
from bs4 import BeautifulSoup
import re
# from app.src.url import *

def url_search_generator(shop, category, product_name):   # !!!may need changes!!!
    if shop == 'emag':
        return 'https://www.emag.ro/search/' + category + '/stoc/vendor/emag/' + '+'.join(product_name.strip().split())
    return None

def get_plain_text(parent):
    if parent is None:
        return ''
    return ''.join(x.strip() + ' ' for x in parent.find_all(text=True, recursive=False)).strip()

def find_whole_word(text, word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(text)

def verify_card_title(title, searched_title):
    title = title.lower()
    searched_title = searched_title.lower()
    for token in searched_title.strip().split():
        if find_whole_word(title, token) is None:
            return False
    return True

def get_data_from_card(html_card, searched_title): # !!!may need changes!!!
    title = html_card.find('a', class_='product-title js-product-url')

    if not verify_card_title(get_plain_text(title), searched_title):
        return

    old_price = html_card.find('p', class_='product-old-price').find('s')
    new_price = html_card.find('p', class_='product-new-price')
    link_to_product = title['href']
    print('Title: ' + get_plain_text(title))
    print('Old price: ' + get_plain_text(old_price))
    print('New price: ' + get_plain_text(new_price))
    print('Link: ' + link_to_product)
    print('--------------------------------')

def run():
    # category = input('Category: ').strip()
    category = 'telefoane-mobile'
    # name = input('Name: ').strip()
    name = 'iphone x 64gb'
    url = url_search_generator('emag', category, name)
    try:
        response = requests.get(url)
        html_data = response.content
        soup = BeautifulSoup(html_data, 'html.parser')

        for html_card in soup.find_all('div', class_='card-item js-product-data'):
            get_data_from_card(html_card, name)
    except ConnectionError as e:
        print(str(e))


run()