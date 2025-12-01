import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional, List


def _perform_swipe(driver):
    """Helper function to perform a standard vertical scroll down."""
    try:
        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        # Define start (80% down) and end (20% down) coordinates for scrolling up the content
        start_x = width // 2
        start_y = int(height * 0.80)
        end_x = width // 2
        end_y = int(height * 0.20)

        # Execute the scroll action
        driver.swipe(start_x, start_y, end_x, end_y, 500)  # 500ms duration
        time.sleep(1)  # Pause to let the UI settle after the scroll

    except WebDriverException as e:
        print(f"⚠️ Warning: Could not perform swipe. Driver error: {e}")


def scroll_down_to_find_an_element(driver, target_name_id, max_swipes):
    """
    Scrolls down the screen until an element with the 'btn_add_products' ID is found,
    or until the end of the page is reached.
    """
    print(f"Searching for element : {target_name_id}")

    previous_page_source = ""

    for i in range(max_swipes):
        print(f"--- Scroll attempt {i + 1} of {max_swipes} ---")

        # 1. CHECK FOR THE ELEMENT
        # We use find_elements() which returns a list (non-failing check)
        element = driver.find_elements(AppiumBy.ID, target_name_id)

        if element.is_displayed:
            print(f"✅ SUCCESS! Found button on the current screen (State: {element.text.upper()}).")
            return element  # Return the first element found

        # 2. CHECK FOR END OF PAGE
        current_page_source = driver.page_source
        if current_page_source == previous_page_source:
            print("🛑 Reached end of the page (Page source did not change). Stopping search.")
            break  # Exit the loop

        previous_page_source = current_page_source

        # 3. PERFORM SCROLL
        print("Scrolling down...")
        _perform_swipe(driver)

    print("❌ FAILED. Max scrolls reached or element not found on page.")
    return None

# --- Example Usage (Assuming driver and wait are initialized) ---
#
# found_button = scroll_to_find_add_button(driver)
# if found_button:
#     # The button is found, regardless of its text (Locked, Sold, or Add)
#     print(f"Found button with text: {found_button.text}")
# else:
#     print("The product button was not found anywhere on the page.")