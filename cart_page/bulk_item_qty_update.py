import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def bulk_item_qty_update(driver, wait):
    try:
        print("\n--- Starting Bulk Quantity Update ---")

        # 1. Find all product names to determine the total item count
        product_elements = wait.until(EC.presence_of_all_elements_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="product name"]')
        ))
        total_items = len(product_elements)
        print(f"📦 Total items found in cart: {total_items}")

        # 2. Loop through each item by its index
        # Note: XPath indices start at 1
        for i in range(1, total_items + 1):
            print(f"\nProcessing Item {i}...")

            # Locate the product name for logging purposes
            item_name = driver.find_element(AppiumBy.XPATH,
                                            f'(//android.widget.TextView[@resource-id="product name"])[{i}]').text

            # A. Get the initial quantity for THIS specific item
            qty_xpath = f'(//android.widget.TextView[@resource-id="product quantity"])[{i}]'
            initial_qty_text = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, qty_xpath))).text
            initial_qty = int(initial_qty_text.strip())

            # B. Define clicks for this item
            clicks_to_perform = 1
            plus_btn_xpath = f'new UiSelector().resourceId("product quantity plus").instance({i-1})'
            plus_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, plus_btn_xpath)))

            # C. Perform Clicks
            for _ in range(clicks_to_perform):
                plus_btn.click()
                time.sleep(1.5)  # Wait for backend sync/UI update

            # D. Verify the update for THIS item
            # We re-fetch the text using the same index-based XPath
            final_qty_text = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, qty_xpath))).text
            final_qty = int(final_qty_text.strip())

            expected_qty = initial_qty + clicks_to_perform

            if final_qty == expected_qty:
                print(f"✅ {item_name}: Successfully updated from {initial_qty} to {final_qty}")
            else:
                print(f"❌ {item_name}: Mismatch! Expected {expected_qty}, got {final_qty}")

        print("\n--- Bulk Update Completed ---")

    except Exception as e:
        print(f"❌ Error during bulk update: {e}")