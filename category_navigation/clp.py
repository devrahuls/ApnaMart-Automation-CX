import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def horizontal_scroll_category_pane(driver, wait, text):
    """
        Scroll horizontally on category pane until an element with given text is found.
    """
    # window_size = driver.get_window_size()
    # width = window_size["width"]
    # height = window_size["height"]
    #
    # start_x = int(width * 0.8) #right part of the screen
    # end_x = int(width * 0.2) #left part of the screen
    # y = int(height * 0.25) #height of the screen from top
    #
    # max_swipes = 7 #maximum number of swipes to be done.
    #
    # for i in range(max_swipes):
    #     try:
    #         el = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
    #         return wait.until(EC.visibility_of(el))
    #     except NoSuchElementException:
    #         # Swipe right
    #         driver.swipe(start_x, y, end_x, y, 800)
    #
    #
    # raise Exception(f"Element with text '{text}' not found after {max_swipes} swipes")
    """
        Uses Android native UiScrollable to scroll horizontally to the element.
        """
    try:
        # UiScrollable syntax:
        # 1. Select the scrollable container
        # 2. Set direction to Horizontal
        # 3. Scroll until the text is found
        android_script = (
            f'new UiScrollable(new UiSelector().resourceId("com.apnamart.apnaconsumer:id/categoryPaneList"))'
            f'.setAsHorizontalList()'
            f'.scrollIntoView(new UiSelector().text("{text}"))'
        )

        el = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, android_script)
        return wait.until(EC.visibility_of(el))

    except Exception as e:
        raise Exception(f"Element with text '{text}' not found via UiScrollable. Error: {str(e)}")

def clickOnCategoriesPane(wait, text):

    # el = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.view.ViewGroup").instance(12)')))
    # el.click()

    categories_button = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector()'
    '.resourceId("com.apnamart.apnaconsumer:id/tvCategory")'
        f'.text("{text}")')
        )
    )
    categories_button.click()
    print(f"✅ Found {text.upper()} button, clicking it.")


def click_on_first_category(wait, text):
    first_category = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/imageView").instance(0)')))
    first_category.click()
    print("✅ Clicking on the very first category.")

    add_item = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddBig").instance(0)')))
    add_item.click()

    search_from_clp = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/search_btn"))
    )
    search_from_clp.click()

    back_btn_to_clp = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/back_button"))
    )
    back_btn_to_clp.click()

    back_btn_from_clp = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/back_img"))
    )
    back_btn_from_clp.click()


