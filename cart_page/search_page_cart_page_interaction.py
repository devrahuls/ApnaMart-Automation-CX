import time
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy


def search_page_cart_page_interaction(driver, wait):
    try:
        print('Clicking on the Search button...')
        search_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/search_btn"))
        )
        search_btn.click()
        print('✅ Search Page has opened')
    except NoSuchElementException:
        print('❌ No Search Button has found')

    # enter the name of the item to search for.
    item_name = 'milk'
    try:
        search_input = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
        )
        search_input.send_keys(item_name)
    except TimeoutException:
        print('No search bar found')

    # waiting time till the item got searched and add button is availabe to interact
    time.sleep(2)

    print(f"--- Capturing details for: {item_name} ---")
    searched_product_names = ''
    searched_product_prices = ''
    searched_product_quantities = ''
    # 1. Capture details FIRST (while the screen is static)
    print(f"--- Capturing details for: {item_name} ---")
    try:
        # Use visibility_of_element_located for better stability
        name_el = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH,
                                                               '//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/productName"]')))
        searched_product_names = name_el.text

        price_el = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH,
                                                                '//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/tvProductOfferPrice"]')))
        searched_product_prices = price_el.text

        print(f"Captured: {searched_product_names} | {searched_product_prices}")

    except Exception as e:
        print(f"❌ Failed to capture details: {e}")

    # 2. NOW click the Add button
    try:
        add_item = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                                          'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddToCart").instance(0)')))
        add_item.click()
        print(f"✅ Item '{item_name}' added to cart.")

        # After clicking, the Qty will appear or update
        time.sleep(1)  # Small buffer for the qty counter to render
        try:
            qty_el = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tvCount")))
            searched_product_quantities = qty_el.text
        except:
            searched_product_quantities = '1'

    except NoSuchElementException:
        print("❌ Add button not found")

    try:
        back_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/back_button"))
        )
        back_btn.click()
        print('Opens the Cart Page')
    except TimeoutException:
        print('Could not find the back btn')

    print("Waiting for Cart Page to stabilize...")
    time.sleep(2)

    expected_name = searched_product_names.strip()
    expected_price = searched_product_prices.strip()
    expected_qty = str(searched_product_quantities).strip()

    try:
        # Use the FULL resource-id found in Appium Inspector for the Cart Page
        cart_names = wait.until \
            (EC.presence_of_all_elements_located(
                (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="product name"]')))
        cart_prices = wait.until \
            (EC.presence_of_all_elements_located(
                (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="product sp"]')))
        cart_qtys = wait.until(EC.presence_of_all_elements_located
                               ((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="product quantity"]')))

        item_found = False

        for i in range(len(cart_names)):
            current_cart_name = cart_names[i].text.strip()
            current_cart_price = cart_prices[i].text.strip()
            current_cart_qty = cart_qtys[i].text.strip()

            # Check if this specific row matches our added item
            if current_cart_name == expected_name:
                item_found = True
                print(f"✅ Found '{expected_name}' at index {i} in the cart.")

                # Now verify price and qty for this specific found item
                if current_cart_price == expected_price and current_cart_qty == expected_qty:
                    print(f"✅ SUCCESS: Price ({current_cart_price}) and Qty ({current_cart_qty}) match!")
                else:
                    print(f"❌ MISMATCH found for {expected_name}:")
                    print(f"   Expected: Price {expected_price}, Qty {expected_qty}")
                    print(f"   Actual:   Price {current_cart_price}, Qty {current_cart_qty}")
                break  # Exit loop once the item is found and verified

        if not item_found:
            print(f"❌ FAILED: The item '{expected_name}' was not found in the cart at all.")
    except TimeoutException:
        print('Could not find the item')


