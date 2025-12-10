import time
from selenium.common.exceptions import WebDriverException, NoSuchElementException


def scroll_down_to_find_an_element(driver, by, locator, max_scrolls):
    """
    Scrolls down the screen until an element with the 'btn_add_products' ID is found,
    or until the end of the page is reached.
    """
    """
    Scrolls down until the element is found.
    Stops if the end of the scrollable area is reached or max_scrolls limit is hit.
    Works with ANY locator:
        - AppiumBy.ID
        - AppiumBy.XPATH
        - AppiumBy.ANDROID_UIAUTOMATOR
        - AppiumBy.ACCESSIBILITY_ID
    """

    # Get device screen size for swipe
    size = driver.get_window_size()
    start_y = int(size['height'] * 0.8)
    end_y = int(size['height'] * 0.3)
    x = int(size['width'] * 0.5)

    # Variable to store the page source from the previous scroll check
    previous_page_source = ""

    # 1. Initial Attempt
    # Try to find element without scrolling
    try:
        found_element = driver.find_element(by, locator)
        print("✅ Element found on current screen without scrolling.")
        return found_element
    except NoSuchElementException:
        pass  # Element not found, proceed to scroll

    # 2. Start scrolling
    for i in range(max_scrolls):

        # --- End of Page Check ---
        current_page_source = driver.page_source
        if current_page_source == previous_page_source:
            # If the source hasn't changed, we've hit the bottom boundary.
            print("🛑 Reached end of scrollable page (Page source did not change). Stopping search.")
            break

        previous_page_source = current_page_source
        # --- End of Page Check ---

        # Scroll Down (Swipe UP)
        try:
            driver.swipe(x, start_y, x, end_y, 500)
            time.sleep(1)
        except WebDriverException as e:
            print(f"⚠️ Warning: Could not perform swipe. Driver error: {e}")

        # Try again after scroll
        try:
            return driver.find_element(by, locator)
        except NoSuchElementException:
            continue  # Element still not found, continue to next scroll

    # If not found after all scrolls or stopped by end-of-page check
    raise NoSuchElementException(f"Element not found after {max_scrolls} scrolls: {by} -> {locator}")


def scroll_up_to_find_an_element(driver, by, locator, max_scrolls):

    """
    Scrolls down until the element is found or reached the end of the page.
    Stops if the end of the scrollable area is reached or max_scrolls limit is hit.
    Works with ANY locator:
        - AppiumBy.ID
        - AppiumBy.XPATH
        - AppiumBy.ANDROID_UIAUTOMATOR
        - AppiumBy.ACCESSIBILITY_ID
    """

    print(f"Searching for element : {locator}")

    # Get device screen size for swipe
    size = driver.get_window_size()
    start_y = int(size['height'] * 0.8)
    end_y = int(size['height'] * 0.3)
    x = int(size['width'] * 0.5)

    # Variable to store the page source from the previous scroll check
    previous_page_source = ""

    # 1. Initial Attempt
    # Try to find element without scrolling
    try:
        found_element = driver.find_element(by, locator)
        print("✅ Element found on current screen without scrolling.")
        return found_element
    except NoSuchElementException:
        pass  # Element not found, proceed to scroll

    # 2. Start scrolling
    for i in range(max_scrolls):

        # --- End of Page Check ---
        current_page_source = driver.page_source
        if current_page_source == previous_page_source:
            # If the source hasn't changed, we've hit the bottom boundary.
            print("🛑 Reached end of scrollable page (Page source did not change). Stopping search.")
            break

        previous_page_source = current_page_source
        # --- End of Page Check ---

        # Scroll Down (Swipe UP)
        try:
            driver.swipe(x, start_y, x, end_y, 500)
            time.sleep(1)
        except WebDriverException as e:
            print(f"⚠️ Warning: Could not perform swipe. Driver error: {e}")

        # Try again after scroll
        try:
            return driver.find_element(by, locator)
        except NoSuchElementException:
            continue  # Element still not found, continue to next scroll

    # If not found after all scrolls or stopped by end-of-page check
    raise NoSuchElementException(f"Element not found after {max_scrolls} scrolls: {by} -> {locator}")
