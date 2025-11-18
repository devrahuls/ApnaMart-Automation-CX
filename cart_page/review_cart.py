from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


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

# --- Example Usage ---
# You would call this function in your test script
# verify_cart_bar()


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
    bottom_cart = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/cartItemsCount'))
    )
    bottom_cart.click()
    print('✅ Review cart bottomsheet has been opened')

    # confirm Review Cart text
    review_cart_text = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Review Cart")'))
    )
    print(f'{review_cart_text.text} is available.')

    #store status
    store_status = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_delivering_in'))
    )
    print(f'Store is currently in {store_status.text} status')

    #  All items count verification on the review cart
    items_count = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_review_cart'))
    )
    print(f'{items_count.text} are in the cart.')


    # quantity counts verification on item(s)
    qty_count_item0 = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/tvCount").instance(0)'))
    )
    print(f'{qty_count_item0.text} qty of first item in the cart.')

    # try:
    #     increase_qty_item0 = wait.until(
    #         EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/tvCount").instance(0)'))
    #     )
    # except:
    #     print()








