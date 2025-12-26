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


def scroll_till_end_of_page(driver, max_scrolls):

        print("--- Starting scroll to bottom ---")

        last_page_source = ""
        scroll_count = 0

        while scroll_count < max_scrolls:
            # 1. Capture the current page state
            current_page_source = driver.page_source

            # 2. Check if the page source is the same as the last scroll
            if current_page_source == last_page_source:
                print(f"✅ Reached the bottom of the page after {scroll_count} scrolls.")
                break

            # 3. Update the tracking variable
            last_page_source = current_page_source

            # 4. Perform the scroll action (Swipe from 80% to 20% of screen height)
            size = driver.get_window_size()
            start_x = size['width'] // 2
            start_y = int(size['height'] * 0.8)
            end_x = size['width'] // 2
            end_y = int(size['height'] * 0.2)

            driver.swipe(start_x, start_y, end_x, end_y, 600)

            # 5. Incremental pause to let new items load
            time.sleep(1.5)
            scroll_count += 1
            print(f"Scrolling... ({scroll_count})")
        else:
            print("⚠️ Reached the max_scrolls limit before finding the absolute bottom.")