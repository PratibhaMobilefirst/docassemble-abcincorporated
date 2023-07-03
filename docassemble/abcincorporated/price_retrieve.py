import stripe
from docassemble.base.util import get_config

stripe.api_key = get_config('stripe secret key')

def retrieve_product_price():
    product = stripe.Price.retrieve("price_1MW2ZeBOgpkiH8jqbVSi8t9W")
    return product.unit_amount / 100  