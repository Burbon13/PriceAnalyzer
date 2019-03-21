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