class ProductData:
    def __init__(self, title, old_price, new_price, product_id, link, date_time, shop='emag', image_link='n/a'):
        self.shop = shop
        self.title = title
        self.old_price = old_price
        self.new_price = new_price
        self.id = product_id
        self.link = link
        self.date_time = date_time
        self.image_link = image_link

    def __str__(self) -> str:
        return 'Title: ' + self.title + '\n' + \
               'Shop: ' + self.shop + '\n' + \
               'Old price: ' + str(self.old_price) + '\n' + \
               'New price: ' + str(self.new_price) + '\n' + \
               'Product id: ' + str(self.id) + '\n' + \
               'Link: ' + self.link + '\n' + \
               'Date: ' + str(self.date_time)


# An user may have some saved products he wants to know about
class User:
    pass


class Product:
    def __init__(self, id, title, link, best_price,
                 current_price, best_price_date, current_price_date,
                 image_link=None, monitored=False):
        self._id = id
        self.title = title
        self.link = link
        self.image_link = image_link
        self.monitored = monitored
        self.best_price = best_price
        self.current_price = current_price
        self.best_price_date = best_price_date
        self.current_price_date = current_price_date

    def __str__(self) -> str:
        return 'Id: ' + str(self._id) + '\n' + \
               'Title: ' + self.title


class History:
    def __init__(self, product_id, old_price, new_price, shop, date):
        self.product_id = product_id
        self.old_price = old_price
        self.new_price = new_price
        self.shop = shop
        self.date = date

    def __str__(self) -> str:
        return 'Product id: ' + str(self.product_id) + '\n' + \
               'Shop: ' + self.shop + '\n' + \
               'Old price: ' + str(self.old_price) + '\n' + \
               'New price: ' + str(self.new_price) + '\n' + \
               'Date: ' + str(self.date)


class PricesDTO:
    def __init__(self, old_price, new_price):
        self.old_price = old_price
        self.new_price = new_price


class Avatar:
    def __init__(self, img_data, product_id):
        self.img_data = img_data
        self.product_id = product_id