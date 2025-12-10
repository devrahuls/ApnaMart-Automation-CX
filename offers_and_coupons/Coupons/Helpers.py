from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
import time
from scroll_until_find_an_element import scroll_down_to_find_an_element



def scroll_until_found_coupon_section(driver, wait):
    # --- Configuration ---
    # Define max attempts to scroll before giving up on finding the area.
    MAX_SCROLLS = 7
    # Define the distance to scroll for repositioning (25% of the screen height)
    REPOSITION_SCROLL_DISTANCE = 0.25


    def is_visible(driver, locator_type, locator_value, timeout=1):
        """Checks if an element is visible within a short timeout without throwing an error."""
        try:
            # Use presence_of_element_located for quick check
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator_value))
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def perform_scroll_action(driver, direction, distance_percent):
        """
        Executes a precise scroll action (UP or DOWN) by a percentage of screen height.
        NOTE: This uses the deprecated `swipe` method for simplicity,
        but for production, W3C Actions should be used.
        """
        window_size = driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]

        # Calculate scroll distance in pixels
        scroll_distance = int(height * distance_percent)

        # Define start/end points near the center of the screen
        mid_x = int(width / 2)
        start_y = int(height * 0.7)  # Start near the bottom for stability
        end_y = int(height * 0.3)  # End near the top

        if direction == "DOWN":
            # Swipe UP: Start lower, end higher (moves content DOWN)
            # We need to simulate a small scroll distance, so we use the calculated distance.
            start_y_swipe = mid_x
            end_y_swipe = mid_x + scroll_distance
            driver.swipe(mid_x, start_y, mid_x, start_y - scroll_distance, 800)
        elif direction == "UP":
            # Swipe DOWN: Start higher, end lower (moves content UP)
            driver.swipe(mid_x, end_y, mid_x, end_y + scroll_distance, 800)
        else:
            raise ValueError("Direction must be 'DOWN' or 'UP'")

    def verify_and_revert_a_and_b(driver, a_locator, b_locator):
        """
        Optimized algorithm to find A, check for B by slight scroll,
        revert scroll, and interact with A.
        """
        A_found = False
        B_found = False
        current_scroll = 0

        # Get screen height once for scroll calculations
        screen_height = driver.get_window_size()["height"]

        print("\n--- Starting Search for Coupon Title ---")

        # 1. Find Element A (Scrolling only if necessary)
        while current_scroll <= MAX_SCROLLS:

            # 1a. CHECK FIRST: See if A is visible
            if is_visible(driver, *a_locator):
                A_found = True
                break

            # 1b. SCROLL ONLY IF NECESSARY
            if current_scroll < MAX_SCROLLS:
                print(f"Coupon Title not found. Scrolling down... (Attempt {current_scroll + 1}/{MAX_SCROLLS})")
                # A simple swipe down is usually sufficient to reveal new content
                perform_scroll_action(driver, "DOWN", 0.8)  # Scroll a large distance down
                time.sleep(1)
                current_scroll += 1
            else:
                break

        # 2. If A is Found, Proceed to Reposition and Check B
        if A_found:
            print("✅ Coupon Title has been found!\n Proceeding to check for Coupon Banner.")

            # B. Position A (Down-Scroll) - Expose B's area
            # Use a small, controlled scroll (e.g., 25% of height)
            print("  -> Repositioning Coupon Title to reveal potential Coupon Banner area.")
            perform_scroll_action(driver, "DOWN", REPOSITION_SCROLL_DISTANCE)
            time.sleep(1)

            # C. Verification for B (Check the newly exposed area)
            if is_visible(driver, *b_locator, timeout=2):
                B_found = True
                print("  -> ✅ Coupon Banner verified as PRESENT.")
            else:
                print("  -> ❌ Coupon Banner verified as NOT present.")

            # D. Reversion (Up-Scroll) - Move view back to original A position
            print("  -> Reverting scroll to place Coupon Title in stable position.")
            perform_scroll_action(driver, "UP", REPOSITION_SCROLL_DISTANCE)
            time.sleep(1)

        # 3. Final Verification and Interaction

        if A_found:
            print("\n--- Interaction Phase ---")
            # A is now positioned at the bottom edge of the visible area (stable position)

            # Re-locate A (necessary because the screen changed)
            try:
                element_a = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(a_locator)
                )
                # Example interaction:
                # element_a.click()
                print(f"Interacted with Coupon Title ({a_locator[1]}).")
            except:
                print("ERROR: Could not re-locate to Coupon Title after reversion.")

        else:
            print("\n❌ Coupon Title could not found within max scrolls. Skipping interaction.\n")

        print(f"\nSummary: Coupon Title found: {A_found}, Coupon Banner found: {B_found}\n")
        return A_found, B_found


    OFFER_CARD_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="potential_offer_card_title"]')
    COUPON_BANNER = (AppiumBy.XPATH, '//android.view.View[@resource-id="coupon_banner"]')
    verify_and_revert_a_and_b(driver, OFFER_CARD_TITLE, COUPON_BANNER)

# function to calculate the cart total
def calculate_cart_total(driver, wait):
    print("\nCalculating Cart Total...")

    # If the cart total section is not present on the current screen then start the scrolling down until found
    to_pay = 'new UiSelector().text("To Pay")'
    # scroll_down_to_find_an_element(driver, wait, AppiumBy.ANDROID_UIAUTOMATOR, to_pay, 5)
    scroll_down_to_find_an_element(driver, AppiumBy.ANDROID_UIAUTOMATOR, to_pay, 10)

    # collect the bill items and their values
    collect_bill_items(driver)

    # TODO - Logic to be written to calculate the cart total on the coupon applied
    print('Done!\n')

    '''
    scroll down till the 'To Pay' comes 
    calc - 
        calc = (item total + all variables) - coupon amt
        To Pay == calc
    '''

def collect_bill_items(driver):
    """
    Collects ALL elements matching the specified XPath using find_elements (plural).
    """
    # 1. Use find_elements (PLURAL) to collect all matches.
    all_bill_items = driver.find_elements(
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="Item Total"]'
    )

    # 2. Check the length of the list to see how many elements were found
    print(f"Found {len(all_bill_items)} bill item rows.")

    # 3. Iterate through the list to print the text/interact with each item
    for index, item in enumerate(all_bill_items):
        try:
            # You can access properties like text, size, etc. for each item
            print(f"Item {index + 1}: Text = {item.text}")
            # Example interaction: item.click()
        except Exception as e:
            print(f"Could not read text from item {index + 1}: {e}")


    # TODO - collect all the bill charges and values, and map the charges -> their values