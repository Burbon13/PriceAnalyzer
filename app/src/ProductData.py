class ProductData:  
    def __init__(self, title, old_price, new_price, product_id, link, data_date_time, shop='emag-default'):
        self.shop = shop
        self.title = title
        self.old_price = old_price
        self.new_price = new_price
        self.product_id = product_id
        self.link = link
        self.data_date_time = data_date_time

    def __str__(self) -> str:
        return 'Title: ' + self.title + '\n' + \
                'Shop: ' + self.shop + '\n' + \
                'Old price: ' + str(self.old_price) + '\n' + \
                'New price: ' + str(self.new_price) + '\n' + \
                'Product id: ' + str(self.product_id) + '\n' + \
                'Link: ' + self.link + '\n' + \
                'Date: ' + str(self.data_date_time)