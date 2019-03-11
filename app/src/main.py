from url_generator import url_search_generator
from shops_data import *
from bs4 import BeautifulSoup
from html_processing import get_data_from_card
import requests


def run():
    name = 'ipad pro 2018'
    url = url_search_generator('emag', shops['emag']['categories']['tablets'], name)
    try:
        response = requests.get(url)
        html_data = response.content
        soup = BeautifulSoup(html_data, 'html.parser')

        for html_card in soup.find_all('div', class_='card-item js-product-data'):
            data = get_data_from_card(html_card, name)
            if data:
                print(data)
    except ConnectionError as e:
        print(str(e))


run()