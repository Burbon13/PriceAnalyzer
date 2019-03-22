class ProductService:
    def __init__(self, product_repo):
        self.product_repo = product_repo
    
    def find_all_products(self):
        return self.product_repo.get_all_products()

    def save(self, *products):
        pass

    def set_monitoring(self, product, state: bool):
        pass

    def delete(self, *products):
        pass

    def current_price(self, product_id: int):
        return self.product_repo.get_current_price(product_id)

    def lowest_price(self, product_id: int):
        return self.product_repo.get_min_price(product_id)

    def get_all_history(self, product_id: int):
        return self.product_repo.get_all_history(product_id)