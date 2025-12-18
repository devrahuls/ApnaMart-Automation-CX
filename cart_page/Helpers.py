import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# --- Data Storage Arrays ---
# These lists will store the data captured from the search results page.
searched_product_names = []
searched_product_prices = []
searched_product_quantities = []

# # These lists will store the data captured from the review cart page.
cart_product_names = []
cart_product_prices = []
cart_product_quantities = []


def search_and_gather_data_add_to_cart(wait, item_name):
    """
    Searches for an item, adds it to the cart, captures the product details
    at the time of search result display, and navigates back.
    """

    # 1. Wait for stable homepage element
    try:
        print("\n--- Starting Search & Add Flow ---")
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/masthead_top"))
        )
        print("✅ Homepage is stable.")
    except TimeoutException:
        print("🛑 Homepage never loaded or stable element not found. Stopping.")
        raise

    # 2. Open the search page and make search bar active
    try:
        search_bar = wait.until(EC.element_to_be_clickable((AppiumBy.ID,
                                                            "com.apnamart.apnaconsumer:id/searchText")))
        search_bar.click()
        print('✅ Search Page has opened.')
    except TimeoutException:
        print("❌ No search bar found")

    # 3. Enter the name of the item to search for.
    try:
        search_input = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
        )
        search_input.send_keys(item_name)
    except TimeoutException:
        print('❌ No search input element found')

    # 4. Wait for search results to load
    time.sleep(3)

    # 5. Click Add btn to add the item in the Cart
    add_item = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                                      'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddToCart").instance(0)')))
    add_item.click()
    print(f"✅ Item '{item_name}' added to cart.")

    # 6. Capture product details for the first item (giving nothing like instance(0)/xpath[1] implies the first result automatically)
    print(f"--- Capturing details for: {item_name} ---")
    try:
        # Get Name
        name_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH,
            '//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/productName"]'))
        )
        searched_product_names.append(name_element.text)
        print(f"Captured Name: {name_element.text}")

        # Get Price
        price_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH,
            '(//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/tvProductOfferPrice"])'))
        )
        searched_product_prices.append(price_element.text)
        print(f"Captured Price: {price_element.text}")

        # Get Quantity (The AddToCart button doesn't always show quantity, assuming 1 on first add)
        # However, for an accurate match, we need to read the initial quantity.
        # If the quantity is NOT displayed before clicking 'Add to Cart', you may have to assume '1'.
        # Since the provided code has no qty capture before clicking 'Add', we'll read '1' from a hypothetical 'tvCount' if available.
        # If 'tvCount' is not visible yet, we assume a starting qty of '1' for the search result.
        # For simplicity in this example, we will assume it defaults to '1' or read the value if available.

        try:
            qty_element = wait.until(
                EC.presence_of_element_located((AppiumBy.ID,
                "com.apnamart.apnaconsumer:id/tvCount"))
            )
            searched_product_quantities.append(qty_element.text)
        except TimeoutException:
            # If the quantity element (tvCount) is not yet displayed (i.e., only 'Add' button is there)
            # we assume the first add will result in 1 item.
            searched_product_quantities.append('1')

        print(f"Captured Qty: {searched_product_quantities[-1]}")


    except (NoSuchElementException, TimeoutException) as e:
        print(f"❌ Failed to find product details or AddToCart button: {e}")
        # Append placeholder or fail the test depending on your test strategy
        searched_product_names.append("FAIL")
        searched_product_prices.append("FAIL")
        searched_product_quantities.append("FAIL")

    # 7. Navigate back to homepage
    try:
        back_btn_to_homepage = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/back_button"))
        )
        back_btn_to_homepage.click()
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/masthead_top"))
        )
        print("✅ Back to stable homepage.")
    except (NoSuchElementException, TimeoutException):
        print("❌ Could not click back button or return to homepage.")

    print(f'✅ Item name: {item_name} has been processed.')


def review_cart_item_verification(wait):
    """
    Opens the review cart, extracts all product details, and prints the result.
    """

    # 1. Find all Name, Price, and Quantity elements in the cart
    try:
        # NOTE: XPath with resource-id is highly robust in Appium/Android
        cart_names = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,
                                                                     '//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/productName"]')))

        cart_prices = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,
                                                                      '//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/tvProductOfferPrice"]')))

        # NOTE: The quantity element ID in the cart is often different from the search result page.
        cart_quantities = wait.until(EC.presence_of_all_elements_located((AppiumBy.XPATH,
                                                                          '//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/tvCount"]')))

        # 2. Store details from the cart into the global arrays
        cart_product_names.clear()  # Clear before refilling
        cart_product_prices.clear()
        cart_product_quantities.clear()

        for element in cart_names:
            cart_product_names.append(element.text)

        for element in cart_prices:
            cart_product_prices.append(element.text)

        for element in cart_quantities:
            cart_product_quantities.append(element.text)

        print(f"\n✅ Successfully extracted {len(cart_product_names)} items from the cart.")

    except TimeoutException:
        print("❌ Failed to find all product elements in the cart. Cart may be empty or elements changed.")
        return
    except StaleElementReferenceException:
        # Handle case where the screen updates while looping
        print("⚠️ Stale element error, retrying cart element capture.")
        review_cart_item_verification(wait)  # Recursive retry (use carefully)
        return

    # 3. Perform the final comparison
    compare_product_data()


def compare_product_data():
    """
    Compares the data captured during search with the data captured from the cart.
    """
    print("--- Starting Data Comparison ---")

    # 1. Check if the number of items matches
    if len(searched_product_names) != len(cart_product_names):
        print(f"❌ FAIL: Item count mismatch! Searched: {len(searched_product_names)}, Cart: {len(cart_product_names)}")
        return

    # 2. Iterate and compare all stored attributes
    all_matched = True
    for i in range(len(searched_product_names)):
        searched_name = searched_product_names[i]
        cart_name = cart_product_names[i]
        searched_price = searched_product_prices[i]
        cart_price = cart_product_prices[i]
        searched_qty = searched_product_quantities[i]
        cart_qty = cart_product_quantities[i]

        # In a real test, you might use fuzzy matching or normalization (e.g., currency removal)
        name_match = searched_name == cart_name
        price_match = searched_price == cart_price
        qty_match = searched_qty == cart_qty

        # Overall item match status
        item_match = name_match and price_match and qty_match

        print(f"\n--- Item {i + 1} Comparison ---")
        print(f"Name Match: {name_match} | Searched: '{searched_name}' | Cart: '{cart_name}'")
        print(f"Price Match: {price_match} | Searched: '{searched_price}' | Cart: '{cart_price}'")
        print(f"Qty Match: {qty_match} | Searched: '{searched_qty}' | Cart: '{cart_qty}'")

        if not item_match:
            print(f"❌ FAIL: Item {i + 1} data mismatch!")
            all_matched = False
        else:
            print(f"✅ SUCCESS: Item {i + 1} data fully matched.")

    print("\n--- Final Test Result ---")
    if all_matched:
        print("🎉 TEST PASSED: All searched items matched their details in the cart.")
    else:
        print("🛑 TEST FAILED: One or more item details did not match.")