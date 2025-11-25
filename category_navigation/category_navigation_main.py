import time

from category_navigation.clp import clickOnCategoriesPane, horizontal_scroll_category_pane, click_on_first_category

def category_navigation_main(driver, wait):
    time.sleep(3)
    horizontal_scroll_category_pane(driver, wait, "Categories")
    clickOnCategoriesPane(wait, "Categories")
    click_on_first_category(wait, "Categories")