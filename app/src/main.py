import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

shops = {
    1: 'emag',
    2: 'altex',
    3: 'mediagalaxy'
}


categories = {
    1: 'laptopuri',
    2: 'telefoane-mobile',
    3: 'tablete',
    4: 'televizoare',
    5: 'boxe-portabile',
    6: 'casti-audio',
    7: 'console-hardware'
}


def url_search_generator(shop, category, product_name):   # !!!may need changes!!!
    if shop == 'emag':
        return 'https://www.emag.ro/search/' + category + '/stoc/vendor/emag/' + '+'.join(product_name.strip().split())
    return None

def get_plain_text(parent):
    if parent is None:
        return '-1'
    return  ''.join(x.strip() + ' ' for x in parent.find_all(text=True, recursive=False)).strip()


def find_whole_word(text, word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(text)


def verify_card_title(title, searched_title):
    title = title.lower()
    searched_title = searched_title.lower()
    for token in searched_title.strip().split():
        if find_whole_word(title, token) is None:
            return False
    return True


class RegexCompiles:
    re_compile_product_id = re.compile('Product-Id=[0-9]*')
    re_compile_id = re.compile('[0-9]+')


def get_product_id(link_to_product):
    s_matched =  RegexCompiles.re_compile_product_id.search(link_to_product).group()
    # id_matched = re.compile('[0-9]*').search(s_matched).group()  '*' finds first string as being empty - matches
    id_matched = RegexCompiles.re_compile_id.search(s_matched).group()
    return int(id_matched)


class ProductData:
    def __init__(self, title, old_price, new_price, product_id, link, data_date_time):
        self.title = title
        self.old_price = old_price
        self.new_price = new_price
        self.product_id = product_id
        self.link = link
        self.data_date_time = data_date_time

    def __str__(self) -> str:
        return 'Title: ' + self.title + '\n' + \
                'Old price: ' + str(self.old_price) + '\n' + \
                'New price: ' + str(self.new_price) + '\n' + \
                'Product id: ' + str(self.product_id) + '\n' + \
                'Link: ' + self.link + '\n' + \
                'Date: ' + str(self.data_date_time)


def get_data_from_card(html_card, searched_title): # !!!may need changes!!!
    title = html_card.find('a', class_='product-title js-product-url')

    if not verify_card_title(get_plain_text(title), searched_title):
        return

    old_price = int(get_plain_text(html_card.find('p', class_='product-old-price').find('s')).replace('.',''))
    new_price = int(get_plain_text(html_card.find('p', class_='product-new-price')).replace('.',''))
    link_to_product = title['href']
    product_id = get_product_id(link_to_product)
    product_data = ProductData(get_plain_text(title), old_price, new_price, product_id, link_to_product, datetime.now())
    print(product_data)
    print('--------------------------------------')


def run():
    # category = input('Category: ').strip()
    # name = input('Name: ').strip()
    name = 'ipad pro 2018'
    url = url_search_generator(shops[1], categories[3], name)
    try:
        response = requests.get(url)
        html_data = response.content
        soup = BeautifulSoup(html_data, 'html.parser')

        for html_card in soup.find_all('div', class_='card-item js-product-data'):
            get_data_from_card(html_card, name)
    except ConnectionError as e:
        print(str(e))


run()
# print(datetime.now())

#print(get_product_id('https://www.emag.ro/apple-ipad-pro-2018-11-256gb-cellular-silver-mu172hc-a/pd/DJNSR4BBM/?X-Search-Id=ae9e2db81b7196c66864&X-Product-Id=5115157&X-Search-Page=1&X-Search-Position=6&X-Section=search&X-MB=0&X-Search-Action=view'))