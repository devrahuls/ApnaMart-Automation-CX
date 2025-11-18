import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def horizontal_scroll_category_pane(driver, wait):
    """
            Scroll vertically from screen center until element with given text is found.
            """
    window_size = driver.get_window_size()
    width = window_size["width"]
    height = window_size["height"]

    # start_x = width // 2
    # start_y = int(height * 0.7)  # lower part of screen
    # end_y = int(height * 0.3)  # upper part of screen

    start_x = int(width * 0.8)
    end_x = int(width * 0.2)
    y = int(height * 0.25)

    text = "Categories"
    max_swipes = 5

    for i in range(max_swipes):
        try:
            el = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
            return wait.until(EC.visibility_of(el))
        except NoSuchElementException:
            # Swipe up

            driver.swipe(start_x, y, end_x, y, 800)


    raise Exception(f"Element with text '{text}' not found after {max_swipes} swipes")

def clickOnCategoriesPane(wait):

    # el = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.view.ViewGroup").instance(12)')))
    # el.click()

    categories_button = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector()'
    '.resourceId("com.apnamart.apnaconsumer:id/tvCategory")'
        '.text("Categories")')
        )
    )
    categories_button.click()
    print("✅ Found 'Categories' button, clicking it.")

    first_category = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/imageView").instance(0)')))
    first_category.click()
    print("✅ Clicking on the very first category.")

    add_item = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddBig").instance(0)')))
    add_item.click()



    # try:
    #     """
    #     Scroll vertically from down to up at screen center.
    #     """
    #     window_size = driver.get_window_size()
    #     width = window_size["width"]
    #     height = window_size["height"]
    #
    #     start_x = width // 2
    #     start_y = int(height * 0.5)  # lower part of screen
    #     end_y = int(height * 0.4)  # upper part of screen
    #
    #     driver.swipe(start_x, start_y, start_x, end_y, 800)
    #
    # except (WebDriverException, KeyError) as e:
    #     print(f"❌ Error during horizontal scroll: {e}")
    #     raise

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


