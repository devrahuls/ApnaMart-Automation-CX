from offers_and_coupons.Coupons.coupon_verification import coupon_verification_main, product_reward_coupon_verification
from scroll_until_find_an_element import scroll_down_to_find_an_element, scroll_up_to_find_an_element
from search_and_browse.search_and_add_to_cart_flow import search_and_add_to_cart_flow
from cart_page.view_cart import view_cart




def coupons_main(driver, wait):
    item_name = 'murmure'
    search_and_add_to_cart_flow(wait, item_name)
    view_cart(wait)


    product_reward_coupon_verification(driver, wait)

    # coupon_verification_main(driver, wait)




