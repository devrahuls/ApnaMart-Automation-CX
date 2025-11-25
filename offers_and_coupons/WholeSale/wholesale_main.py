from cart_page.view_cart import view_cart
from offers_and_coupons.WholeSale.wholesale_verification import wholesale_verification
from search_and_browse.search_and_add_to_cart_flow import search_and_add_to_cart_flow
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from category_navigation.clp import horizontal_scroll_category_pane, clickOnCategoriesPane


def wholesale_main(driver, wait):
    horizontal_scroll_category_pane(driver, wait, 'WholeSale')
    clickOnCategoriesPane(wait, 'WholeSale')
    wholesale_verification(wait)