from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException



def view_cart(wait):
    # View cart
    try:
        view_cart_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/viewCart'))
        )
        view_cart_btn.click()
        print('Opening Cart Page...')
    except TimeoutException:
        print('Failed to open cart page.')

def qty_update(driver, wait):
    int_max = 2**31 - 1

    for i in range(2, int_max):

        qty_plus = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btAdd'))
        )
        qty_plus.click()

        item_qty = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tvCount'))
        )
        item_qty_val = item_qty.text

        if item_qty_val != i:
            print(f'You cant purchase more than {item_qty_val} quantity of this item.')
            break


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


def verify_empty_cart(wait):
    qty_minus = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btMinus'))
    )
    qty_minus.click()

    cart_empty = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/noItemsText'))
    )
    print(f'✅ {cart_empty.text} text is available!')

    start_shopping_home_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/homeButton'))
    )
    start_shopping_home_btn.click()

    print('✅ Empty cart is working fine, successfully redirected to home page after clicking start shopping btn.')