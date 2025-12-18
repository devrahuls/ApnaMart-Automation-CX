from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scroll_until_find_an_element import scroll_down_to_find_an_element

'''
TODO: this function is just a blueprint, need to add the actual values.
'''
def verify_cart_bill_toggle(driver, wait: WebDriverWait):
    """
    Verifies that the cart bill attributes and values are preserved
    when the cart bill is toggled (hidden and then revealed).
    """

    # --- LOCATORS ---
    LOCATOR_ATTRIBUTES = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="bill_item_row"]'
    LOCATOR_VALUES = AppiumBy.XPATH, '//android.widget.TextView[@text="Item Total Value"]'
    LOCATOR_TOGGLE_BTN = AppiumBy.XPATH, '//android.view.View[@resource-id="cartbilltogglebtn"]'

    print("\n--- Starting Cart Bill Toggle Verification ---")

    # 1. GATHER ALL CART BILL ATTRIBUTES AND THEIR VALUES
    try:
        # A. Gather Attribute Elements
        attribute_elements = wait.until(
            EC.presence_of_all_elements_located(LOCATOR_ATTRIBUTES)
        )
        # B. Gather Value Elements (assuming they are 1:1 match in order)
        value_elements = wait.until(
            EC.presence_of_all_elements_located(LOCATOR_VALUES)
        )

        # Extract text into lists A and B
        A_attributes = [el.text for el in attribute_elements if el.text]
        B_values = [el.text for el in value_elements if el.text]

        if not A_attributes or len(A_attributes) != len(B_values):
            print("⚠️ Initial cart bill found, but lists are mismatched or empty after extraction.")
            # For the purpose of the test, we'll proceed if we have at least one pair.
            if len(A_attributes) < 1:
                raise NoSuchElementException("Cart bill elements not properly gathered initially.")

        print(f"✅ Step 1: Gathered initial cart bill data ({len(A_attributes)} items).")
        print(f"   Attributes (A): {A_attributes}")
        print(f"   Values (B): {B_values}")

    except TimeoutException:
        print("🛑 Error: Initial cart bill not found. Cannot proceed with verification.")
        raise NoSuchElementException("Cart bill elements could not be located on the screen.")

    # 2. TOGGLE THE CART BILL (HIDE)
    try:
        toggle_button = wait.until(EC.element_to_be_clickable(LOCATOR_TOGGLE_BTN))
        toggle_button.click()
        print("✅ Step 2: Toggled cart bill (Expected: Hidden).")
    except TimeoutException:
        print("🛑 Error: Cart bill toggle button not found.")
        raise

    # 3. CONFIRM THERE IS NO CART BILL ATTRIBUTES (CONFIRM HIDDEN)
    try:
        # Check if attribute elements are *no longer* present or visible
        # We use a very short explicit wait here to confirm disappearance quickly.
        temp_wait = WebDriverWait(driver, 3)

        # If this line succeeds, the elements are still present (FAIL)
        temp_wait.until(
            EC.presence_of_element_located(LOCATOR_ATTRIBUTES)
        )

        # If we reach here, the elements were found, meaning the toggle FAILED to hide them.
        # 5. IF NO (Cart bill attributes were still found), RAISE AN ERROR
        print("🛑 Step 3 Failed: Cart bill attributes were STILL found after toggling. Toggle function is broken.")
        raise AssertionError("Cart bill toggle failed to hide the elements.")

    except TimeoutException:
        # This is the SUCCESS path: The elements disappeared, so the check timed out.
        print("✅ Step 3: Confirmed cart bill attributes are NOT present (Expected: Hidden).")

        # 4. IF YES (Attributes are hidden), THEN AGAIN TOGGLE THE CART BILL (SHOW)
        try:
            # Re-locate and click the toggle button (it should still be the same element)
            toggle_button = wait.until(EC.element_to_be_clickable(LOCATOR_TOGGLE_BTN))
            toggle_button.click()
            print("✅ Step 4: Toggled cart bill again (Expected: Visible).")

            # 4a. SCROLL TILL THE LAST CARTBILL ATTRIBUTE
            to_pay = 'new UiSelector().text("To Pay")'

            scroll_down_to_find_an_element(driver, AppiumBy.ANDROID_UIAUTOMATOR, to_pay, 10)


            # 4b. MATCH ALL CART BILL ATTRIBUTES AND THEIR VALUES

            # Wait for the elements to reappear
            attribute_elements_reappeared = wait.until(
                EC.presence_of_all_elements_located(LOCATOR_ATTRIBUTES)
            )
            value_elements_reappeared = wait.until(
                EC.presence_of_all_elements_located(LOCATOR_VALUES)
            )

            # Extract new data
            A_attributes_new = [el.text for el in attribute_elements_reappeared if el.text]
            B_values_new = [el.text for el in value_elements_reappeared if el.text]

            print(f"   Re-gathered new attributes (A'): {A_attributes_new}")
            print(f"   Re-gathered new values (B'): {B_values_new}")

            # Compare lists
            if A_attributes == A_attributes_new and B_values == B_values_new:
                print("🎉 SUCCESS: Cart bill attributes and values match after toggling!")
            else:
                print("🛑 FAIL: Cart bill data changed after toggling.")
                print(f"   Original Attributes (A): {A_attributes}")
                print(f"   New Attributes (A'):   {A_attributes_new}")
                print(f"   Original Values (B):   {B_values}")
                print(f"   New Values (B'):       {B_values_new}")
                raise AssertionError("Cart bill data was altered during the toggle sequence.")

        except TimeoutException:
            print("🛑 Error: Cart bill elements did not reappear after the second toggle.")
            raise

    # 5. IF NO (Cart bill attributes were still found, handled inside the initial except)
    # The error is raised inside the 'try' block above if elements are found.

    print("\n--- Cart Bill Toggle Verification Complete ---")

# Example Usage (assuming 'driver' and 'wait' are already defined):
# from selenium import webdriver
# driver = webdriver.Remote(...) # Your Appium setup
# wait = WebDriverWait(driver, 10)
# verify_cart_bill_toggle(driver, wait)