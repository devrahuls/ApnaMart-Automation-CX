import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from cart_page.Helpers import review_cart_item_verification
from cart_page.view_cart import view_cart


# Assume 'driver' is your initialized Appium driver
# Assume 'wait' is your WebDriverWait instance, e.g., wait = WebDriverWait(driver, 10)


def qty_updatee(driver, wait):
    int_max = 2 ** 31 - 1

    # We need to get the *current* quantity to know where to start the loop
    try:
        item_qty_element = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tvCount'))
        )
        # Start the loop from the next number
        start_i = int(item_qty_element.text) + 1
        print(f"Starting quantity check from {start_i}")

    except Exception as e:
        print(f"Could not read initial quantity: {e}")
        start_i = 2  # Default to 2 if reading fails

    try:
        for i in range(start_i, int_max):
            # 1. Click the plus button
            qty_plus = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btAdd'))
            )
            qty_plus.click()

            # 2. Wait for the text to update to the expected number
            expected_text = str(i)

            wait.until(
                EC.text_to_be_present_in_element(
                    (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tvCount'),
                    expected_text
                )
            )
            # If the wait succeeds, the text is now str(i), so we continue the loop

    except TimeoutException:
        # This is now the *expected* way to break the loop.
        # The 'wait.until(EC.text_to_be_present_in_element...)' failed.
        # This means the quantity limit has been reached.

        # We just need to read the final quantity one last time
        final_qty = driver.find_element(AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tvCount').text
        print(f'You cant purchase more than {final_qty} quantity of this item.')

    except StaleElementReferenceException:
        # If this *still* happens, it's a very fast UI.
        # We can just read the final text.
        final_qty = driver.find_element(AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tvCount').text
        print(f'Hit quantity limit at {final_qty} (stale element fallback).')

    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def verify_cart_bar(driver, wait):
    """
    Verifies the three key elements in the cart bar at the bottom of the screen.
    """
    print("--- Starting Cart Bar Verification ---")

    # 1. Verify the Product Image is visible
    try:
        # NOTE: Replace 'product_image_in_cart_bar' with the actual resource-id from Appium Inspector
        product_image = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/product_image_in_cart_bar"))
        )
        print("✅ SUCCESS: Product image is visible.")
    except TimeoutException:
        print("❌ FAILED: Product image was not found.")

    # 2. Verify the Item Count text is correct
    try:
        # NOTE: Replace 'item_count_text' with the actual resource-id
        item_count_element = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/item_count_text"))
        )

        # We can add an extra check to verify the exact text
        if "1 Item" in item_count_element.text:
            print(f"✅ SUCCESS: Item count text is visible and correct ('{item_count_element.text}').")
        else:
            print(f"❌ FAILED: Item count text found, but the text is incorrect ('{item_count_element.text}').")

    except TimeoutException:
        print("❌ FAILED: Item count text was not found.")

    # 3. Verify the "View Cart" button is present and clickable
    try:
        # We can find this button by its visible text
        view_cart_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("View Cart")'))
        )
        print("✅ SUCCESS: 'View Cart' button is visible and clickable.")
    except TimeoutException:
        print("❌ FAILED: 'View Cart' button was not found or is not clickable.")

    print("--- Verification Complete ---")



def verify_small_review_cart_one_item(wait):
    item_img_single = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/img_single_product'))
    )
    print('✅ Single Image available for Single Product in the Cart')

    item_qty_single = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/cartItemsCount'))
    )
    print(f'✅ {item_qty_single.text} count is available.')

def verify_small_review_cart_two_item(wait):
    item_img_double = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/img_double_product'))
    )
    print('✅ Two Images available for Two Product in the Cart')

    item_qty_double = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/cartItemsCount'))
    )
    print(f'✅ {item_qty_double.text} qty count is available.')


# when 3 or more than 3 items are being added in the cart
def verify_small_review_cart_more_item(wait):
    item_img_more_than_three = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/img_more_product'))
    )
    print('✅ Three or more images available for Three or more Product in the Cart')

    item_qty_more_than_three = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/cartItemsCount'))
    )
    print(f'✅ {item_qty_more_than_three.text} qty count is available.')


def review_cart_verification(wait):
    print("\n\n--- Starting Review Cart Flow ---")

    bottom_cart = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/cartItemsCount'))
    )
    bottom_cart.click()
    print('✅ Review cart bottomsheet has been opened')

    # confirm Review Cart text
    review_cart_text = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Review Cart")'))
    )
    print(f'✅ {review_cart_text.text} text heading is available.')

    #store status
    store_status = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_delivering_in'))
    )
    print(f'✅ Store is currently in {store_status.text} status')

    #  All items count verification on the review cart
    total_items_count_and_amt = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_review_cart'))
    )
    print(f'Total {total_items_count_and_amt.text} are in the cart.')

    # verify that the items that have been addded from the search page is same displaying on the review cart
    review_cart_item_verification(wait)


    print("\n--- Review Cart Verification & Modification ---")

    # ... (Your existing code to open bottom sheet and verify store status) ...

    # 1. Update Quantity of the first two items
    # We increase them by clicking the '+' button once for each
    updated_items = {}  # Store {Product Name: Expected Qty}

    for i in range(1, 3):  # XPath index 1 and 2
        try:
            name_xpath = f'(//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/productName"])[{i}]'
            plus_btn_xpath = f'(//android.widget.Button[@resource-id="com.apnamart.apnaconsumer:id/btAdd"])[{i}]'
            qty_xpath = f'(//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/tvCount"])[{i}]'

            item_name = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, name_xpath))).text
            plus_btn = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, plus_btn_xpath)))

            plus_btn.click()
            time.sleep(1)  # Wait for UI to update qty

            new_qty = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, qty_xpath))).text
            updated_items[item_name] = new_qty
            print(f"➕ Updated '{item_name}' to quantity: {new_qty}")
        except Exception as e:
            print(f"❌ Failed to update item {i}: {e}")

    # 2. Remove the next two items
    # Note: When you remove item #3, the old item #4 usually becomes the new item #3.
    # To be safe, we always click the '-' button on index 3 until it disappears.
    removed_items_names = []
    for _ in range(2):
        try:
            # Capture name of the item we are about to remove
            name_to_remove = wait.until(EC.presence_of_element_located((AppiumBy.XPATH,
                                                                        '(//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/productName"])[3]'))).text

            minus_btn = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH,
                                                               '(//android.widget.Button[@resource-id="com.apnamart.apnaconsumer:id/btMinus"])[3]')))

            # Assuming clicking minus when qty is 1 removes the item
            minus_btn.click()
            removed_items_names.append(name_to_remove)
            print(f"🗑️ Removed item: {name_to_remove}")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Failed to remove an item: {e}")

    # 3. Open the full Cart Page
    view_cart(wait)

    # 4. Final Verification on Cart Page
    verify_final_cart_page(wait, updated_items, removed_items_names)


def verify_final_cart_page(wait, expected_updates, removed_names):
    print("\n--- Final Verification on Cart Page ---")

    try:
        # Find all current products on the cart page
        current_names = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,
                                                                        '//android.widget.TextView[@resource-id="product name"]')))
        current_qtys = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,
                                                                       '//android.widget.TextView[@resource-id="product quantity"]')))

        # Convert to a dictionary for easy comparison
        actual_cart_state = {}
        for name_el, qty_el in zip(current_names, current_qtys):
            actual_cart_state[name_el.text] = qty_el.text

        # CHECK 1: Verify Updated Quantities
        for name, expected_qty in expected_updates.items():
            if name in actual_cart_state:
                if actual_cart_state[name] == expected_qty:
                    print(f"✅ MATCH: '{name}' has correct qty {expected_qty}")
                else:
                    print(f"❌ MISMATCH: '{name}' expected {expected_qty} but found {actual_cart_state[name]}")
            else:
                print(f"❌ ERROR: Updated item '{name}' not found on Cart Page!")

        # CHECK 2: Verify Removal
        for name in removed_names:
            if name in actual_cart_state:
                print(f"❌ FAILURE: Removed item '{name}' is still present in cart!")
            else:
                print(f"✅ SUCCESS: Item '{name}' is correctly absent from cart.")

    except Exception as e:
        print(f"❌ Verification failed: {e}")



