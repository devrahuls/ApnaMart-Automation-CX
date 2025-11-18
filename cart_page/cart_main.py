from cart_page import place_order, review_cart, view_cart
from search_and_browse.search_and_add_to_cart_flow import search_and_add_to_cart_flow
from cart_page.review_cart import verify_small_review_cart_one_item, verify_small_review_cart_two_item, verify_small_review_cart_more_item, review_cart_verification


def cart_main(driver, wait):
    item_name = 'kurkure'
    search_and_add_to_cart_flow(wait, item_name)
    verify_small_review_cart_one_item(wait)

    item_name = 'lays'
    search_and_add_to_cart_flow(wait, item_name)
    verify_small_review_cart_two_item(wait)

    item_name = 'chips'
    search_and_add_to_cart_flow(wait, item_name)
    verify_small_review_cart_more_item(wait)

    item_name = 'oil'
    search_and_add_to_cart_flow(wait, item_name)
    verify_small_review_cart_more_item(wait)

    review_cart_verification(wait)