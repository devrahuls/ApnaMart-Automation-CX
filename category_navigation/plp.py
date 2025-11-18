import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def horizontal_scroll_till_end(driver, wait, max_swipes):
    search_bar = wait.until(EC.element_to_be_clickable((AppiumBy.ID,
                                                        "com.apnamart.apnaconsumer:id/searchText")))
    search_bar.click()
    """
    Performs a horizontal swipe on the screen based on percentages of the screen dimensions.

    Args:
        driver: The Appium WebDriver instance.
        start_x_percent: The horizontal starting point as a percentage of screen width (0.0 to 1.0).
        end_x_percent: The horizontal ending point as a percentage of screen width (0.0 to 1.0).
        y_percent: The vertical position for the swipe as a percentage of screen height (0.0 to 1.0).
        duration: The time in milliseconds for the swipe action.
    """
    try:
        window_size = driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]

        # Calculate pixel coordinates
        start_x = int(width * 0.8)
        end_x = int(width * 0.2)
        y = int(height * 0.25)

        time.sleep(1)
        # Perform the swipe
        # for i in range(5):
        #     driver.swipe(start_x, y, end_x, y, 800)
        # print(f"✅ Swiped horizontally at y-position {y}px from x={start_x}px to x={end_x}px.")


        for i in range(max_swipes):
            # 1. Get page source BEFORE the swipe
            page_source_before_swipe = driver.page_source

            # 2. Perform the swipe
            print(f"➡️  Performing swipe #{i + 1}...")
            driver.swipe(start_x, y, end_x, y, 800)

            # 3. Wait a moment for the UI to settle after the swipe
            time.sleep(0.5)  # This is important to allow animations to finish

            # 4. Get page source AFTER the swipe
            page_source_after_swipe = driver.page_source

            # 5. Compare and break if they are the same
            if page_source_before_swipe == page_source_after_swipe:
                print("✅ End of the horizontal list reached.")
                return  # Exit the function

        print(f"⚠️  Max swipes ({max_swipes}) reached. Exiting scroll.")

    except (WebDriverException, KeyError) as e:
        print(f"❌ Error during horizontal scroll: {e}")
        raise


def vertical_scroll_till_end(driver, max_swipes):
    try:
        """
        Scroll vertically from screen center until element with given text is found.
        """
        window_size = driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]

        start_x = width // 2
        start_y = int(height * 0.7)  # lower part of screen
        end_y = int(height * 0.3)  # upper part of screen

        for i in range(max_swipes):
            # 1. Get page source BEFORE the swipe
            page_source_before_swipe = driver.page_source

            # 2. Perform the swipe
            print(f"⬇️ Swipe #{i + 1}...")
            # Swipe up
            driver.swipe(start_x, start_y, start_x, end_y, 800)

            # 3. Wait a moment for the UI to settle after the swipe
            time.sleep(0.5)  # This is important to allow animations to finish

            # 4. Get page source AFTER the swipe
            page_source_after_swipe = driver.page_source

            # 5. Compare and break if they are the same
            if page_source_before_swipe == page_source_after_swipe:
                print("✅ End of the horizontal list reached.")
                return  # Exit the function

    except (WebDriverException, KeyError) as e:
        print(f"❌ Error during horizontal scroll: {e}")
        raise



def view_plp_page(driver, wait):
    view_all = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/viewAll"))
    )
    view_all.click()

    add_item = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddBig").instance(0)')))
    add_item.click()

    try:
        """
        Scroll vertically from screen center until element with given text is found.
        """
        window_size = driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]

        start_x = width // 2
        start_y = int(height * 0.7)  # lower part of screen
        end_y = int(height * 0.3)  # upper part of screen

        for i in range(50):
            # 1. Get page source BEFORE the swipe
            page_source_before_swipe = driver.page_source

            # 2. Perform the swipe
            print(f"➡️  Performing swipe #{i + 1}...")
            # Swipe up
            driver.swipe(start_x, start_y, start_x, end_y, 800)

            # 3. Wait a moment for the UI to settle after the swipe
            time.sleep(0.5)  # This is important to allow animations to finish

            # 4. Get page source AFTER the swipe
            page_source_after_swipe = driver.page_source

            # 5. Compare and break if they are the same
            if page_source_before_swipe == page_source_after_swipe:
                print("✅ End of the horizontal list reached.")
                break

    except (WebDriverException, KeyError) as e:
        print(f"❌ Error during horizontal scroll: {e}")
        raise

    print("✅ PLP View All Page Scroll & Add to Cart flow completed.")