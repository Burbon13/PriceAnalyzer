import logging
from tkinter import Tk

from Domain import History
from repository.ProductRepository import ProductMongoDbRepository
from service.ProductService import ProductService
from gui.main_menu import MenuWindow

from datetime import datetime

def main():
    # logging.basicConfig(format='%(levelname)s|%(asctime)s|%(filename)s:%(funcName)s:%(lineno)d|%(message)s', level=logging.INFO)
    # logging.info('Application started')

    repo = ProductMongoDbRepository('price_manager')

    service = ProductService(repo)

    root = Tk()
    root.geometry("500x400")
    MenuWindow(service, master=root)
    root.mainloop()


main()
