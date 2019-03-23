import re


# Class with static regex compilations
class RegexCompiles:
    # regex for finding product-id in an EMAG link
    re_compile_product_id = re.compile('Product-Id=[0-9]*')
    # regex for finding the first number
    re_compile_id = re.compile('[0-9]+')


# Verifies if a word exists in a text
def find_whole_word(text, word) -> bool:
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(text)


# Verifies if all the words in a given title (given_title) exist in another title (title)
def verify_card_title(title, given_title) -> bool:
    title = title.lower()
    given_title = given_title.lower()
    for token in given_title.strip().split():
        if find_whole_word(title, token) is None:
            return False
    return True


# Returns the product id from an emag link
def get_product_id(link_to_product) -> int:
    s_matched = RegexCompiles.re_compile_product_id.search(link_to_product).group()
    id_matched = RegexCompiles.re_compile_id.search(s_matched).group()
    return int(id_matched)
