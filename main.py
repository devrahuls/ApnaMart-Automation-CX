from cart_page.view_cart import view_cart, qty_update, qty_updatee, verify_empty_cart
from driver_setup import get_driver, get_wait
from Signup.login_flow import login_flow, custom_login
from offers_and_coupons.Best_Deals.best_deals_main import best_deals_main
from search_and_browse.search_and_add_to_cart_flow import search_and_add_to_cart_flow
from store_assignment import store_assignment
from search_and_browse.search_and_browse_main import search_and_browse_main
from category_navigation.pdp import share_product, pdp, product_attributes
from cart_page.review_cart import verify_cart_bar
from cart_page.cart_main import cart_main
from category_navigation.category_navigation_main import category_navigation_main



if __name__ == "__main__":
    driver = get_driver()
    wait = get_wait(driver)

    # Run whichever flows you want
    login_flow(driver, wait)  #MUST
    # custom_login(driver,wait)

    # address = input("Enter address: ")
    store_assignment(driver, wait, "apnamart corporate office")

    # cart_main(driver,  wait)

    # category_navigation_main(driver, wait)

    item_name = 'murmure'
    search_and_add_to_cart_flow(wait, item_name)
    view_cart(wait)
    best_deals_main(driver, wait)
    # search_and_browse_main(wait, item_name)

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
