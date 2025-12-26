# from cart_page.view_cart import view_cart, qty_update, qty_updatee, verify_empty_cart
from driver_setup import get_driver, get_wait
from Signup.login_flow import login_flow, custom_login
from offers_and_coupons.Best_Deals.best_deals_main import best_deals_main
from offers_and_coupons.Coupons.coupons_main import coupons_main
from offers_and_coupons.Special_Price_Deals.spd_main import special_price_deals_main
from offers_and_coupons.WholeSale.wholesale_main import wholesale_main
from search_and_browse.search_and_add_to_cart_flow import search_and_add_to_cart_flow
from store_assignment import store_assignment
from search_and_browse.search_and_browse_main import search_and_browse_main
from category_navigation.pdp import share_product, pdp, product_attributes
from cart_page.review_cart import verify_cart_bar
from cart_page.cart_main import cart_main
from category_navigation.category_navigation_main import category_navigation_main
from Payments.payments_main import payments_main
from cart_page.view_cart import view_cart
from track_order_page import ongoing_track_order_page_verification

from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def disable_android_animations():
    import subprocess

    commands = [
        ["adb", "shell", "settings", "put", "global", "window_animation_scale", "0"],
        ["adb", "shell", "settings", "put", "global", "transition_animation_scale", "0"],
        ["adb", "shell", "settings", "put", "global", "animator_duration_scale", "0"],
    ]

    for cmd in commands:
        subprocess.run(cmd, check=True)

def enable_android_animations():
    import subprocess

    commands = [
        ["adb", "shell", "settings", "put", "global", "window_animation_scale", "1"],
        ["adb", "shell", "settings", "put", "global", "transition_animation_scale", "1"],
        ["adb", "shell", "settings", "put", "global", "animator_duration_scale", "1"],
    ]

    for cmd in commands:
        subprocess.run(cmd, check=True)




if __name__ == "__main__":
    driver = get_driver()
    wait = get_wait(driver)

    disable_android_animations()
    # Run whichever flows you want
    login_flow(driver, wait)  #MUST
    # custom_login(driver,wait)

    enable_android_animations()

    # address = input("Enter address: ")
    store_assignment(driver, wait, "apnamart corporate office")


    # CART PAGE, COUPONS, UPI FAIL, POST ORDER: PAYMENT & TRACK ORDER.
    cart_main(driver,  wait)
    ongoing_track_order_page_verification(driver, wait)
    back_to_hp_from_track_order = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Navigate up")'))
    )
    back_to_hp_from_track_order.click()
    coupons_main(driver, wait)
    back_to_hp_from_cart = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/back_img'))
    )
    back_to_hp_from_cart.click()
    payments_main(driver, wait)
    ongoing_track_order_page_verification(driver, wait)


    # category_navigation_main(driver, wait)


    # item_name = 'murmure'
    # search_and_add_to_cart_flow(wait, item_name)
    # view_cart(wait)
    # best_deals_main(driver, wait)

    # search_and_browse_main(wait, item_name)

    # special_price_deals_main(driver, wait)
    # wholesale_main(driver, wait)







    # verify_cart_bar(driver, wait)

    # pdp(wait)
    # product_attributes(driver, wait)
    # share_product(driver, wait)

    # clickOnCategoriesPane(wait)



    # is_previously_bought_present(wait)
    # previously_bought_view_all(wait)
    # recent_searches(wait)

    # scroll_rail(driver, wait)
    # horizontal_scroll_till_end(driver, wait, 25)
    # view_plp_page(driver, wait)

    # view_cart(driver, wait)
    # place_order_cod(driver, wait, "apnamart corporate office")
    # item_name = 'kurkure'
    # search_and_add_to_cart_flow(wait, item_name)

    # item_name = input("Enter the item name to search: ")
    # search_and_add_to_cart_flow(driver, wait, item_name)
    # home_page_scroll_and_add_to_cart(driver, wait)
    # view_cart(driver, wait)
    # qty_updatee(driver, wait)
    # verify_empty_cart(wait)

    # item_name = 'kurkure'
    # search_and_add_to_cart_flow(wait, item_name)
    # view_cart(driver, wait)


    # place_order_address = input("Enter the place order address: ")
    # place_order_cod(driver, wait, place_order_address)
    #x sleep(6)
    # driver.quit()



# new UiSelector().text("Confirm Location")
