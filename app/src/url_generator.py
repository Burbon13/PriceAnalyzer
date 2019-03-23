# Returns the link generated for a certain search
def url_search_generator(shop, category, product_name) -> str:   # !!!may need changes!!!
    if shop == 'Emag':
        return 'https://www.emag.ro/search/' + category + '/stoc/vendor/emag/' + '+'.join(product_name.strip().split())
    return None