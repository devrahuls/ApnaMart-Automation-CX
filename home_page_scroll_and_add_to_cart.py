from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

# wait_scroll =
def home_page_scroll_and_add_to_cart(driver, wait):
    def scroll_until_text(text, max_swipes=25):
        """
        Scroll vertically from screen center until element with given text is found.
        """
        window_size = driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]

        start_x = width // 2
        start_y = int(height * 0.7)   # lower part of screen
        end_y   = int(height * 0.3)   # upper part of screen

        for i in range(max_swipes):
            try:
                el = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
                return wait.until(EC.visibility_of(el))
            except NoSuchElementException:
                # Swipe up
                driver.swipe(start_x, start_y, start_x, end_y, 800)

        raise Exception(f"Element with text '{text}' not found after {max_swipes} swipes")

    #Call the scroll down function and find the 'Freshener' word
    freshener = scroll_until_text("Fresheners")

    #Press the Add button to add the product on the cart
    add_to_cart_btn = wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddBig").instance(1)'))
    )
    add_to_cart_btn.click()

    print("✅ Home Page Scroll & Add to Cart flow completed.")
