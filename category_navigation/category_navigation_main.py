import time

from category_navigation.clp import clickOnCategoriesPane, horizontal_scroll_category_pane

def category_navigation_main(driver, wait):
    time.sleep(3)
    horizontal_scroll_category_pane(driver, wait)
    clickOnCategoriesPane(wait)