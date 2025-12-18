from appium.webdriver.common.appiumby import AppiumBy

from cart_page.bulk_item_qty_update import bulk_item_qty_update
from cart_page.cancellation_and_refund import cancellation_and_refund_policy
from cart_page.empty_cart import empty_cart_flow
from cart_page.place_order import place_order_cod
from cart_page.review_cart import verify_small_review_cart_one_item, verify_small_review_cart_two_item, verify_small_review_cart_more_item, review_cart_verification
from cart_page.Helpers import search_and_gather_data_add_to_cart
from cart_page.search_page_cart_page_interaction import search_page_cart_page_interaction
from search_and_browse.search_and_add_to_cart_flow import search_and_add_to_cart_flow
from cart_page.view_cart import view_cart
from cart_page.cart_toggle import verify_cart_bill_toggle
from scroll_until_find_an_element import scroll_down_to_find_an_element


def cart_main(driver, wait):
    item_name = 'kurkure'
    search_and_gather_data_add_to_cart(wait, item_name)
    verify_small_review_cart_one_item(wait)

    item_name = 'lays'
    search_and_gather_data_add_to_cart(wait, item_name)
    verify_small_review_cart_two_item(wait)

    item_name = 'chips'
    search_and_gather_data_add_to_cart(wait, item_name)
    verify_small_review_cart_more_item(wait)

    item_name = 'oil'
    search_and_gather_data_add_to_cart(wait, item_name)
    verify_small_review_cart_more_item(wait)

    review_cart_verification(wait)

    search_page_cart_page_interaction(driver, wait)

    bulk_item_qty_update(driver, wait)

    empty_cart_flow(driver, wait)

    item_name = 'kurkure'
    search_and_add_to_cart_flow(wait, item_name)

    view_cart(wait)

    # scroll till the last element of the cart toggle, so that we don't miss any element of it to verify
    by_vct = AppiumBy.ANDROID_UIAUTOMATOR
    locator_vct = 'new UiSelector().resourceId("to_pay")'
    scroll_down_to_find_an_element(driver, by_vct, locator_vct, 10)

    # verify_cart_bill_toggle(driver, wait)
    print("yeay")

    # scroll till the last element of the cart toggle, so that we don't miss any element of it to verify
    by_cnr = AppiumBy.ANDROID_UIAUTOMATOR
    locator_cnr = 'new UiSelector().text("Cancellation & Refund Policy")'
    scroll_down_to_find_an_element(driver, by_cnr, locator_cnr, 10)

    cancellation_and_refund_policy(driver, wait)

    place_order_cod(driver, wait, 'apnamart corporate office' )








