import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from cart_page.view_cart import view_cart
import re


def add_more_products_to_unlock_wh_cart(driver, wait, req_amt_to_unlock):
    print(f'\n{req_amt_to_unlock} amt of item requires to unlock')
    item_name = 'chocolate'
    
    try:
        # Search for item
        search_bar = wait.until(EC.element_to_be_clickable((AppiumBy.ID,"com.apnamart.apnaconsumer:id/searchText")))
        search_bar.click()

        time.sleep(1)

        search_input = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
        )
        search_input.send_keys(item_name)
        print(f'Start searching for {item_name}')
    except Exception as e:
        print(f"No search bar found {e}")


    searched_product_prices = []
    searched_product_prices = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/tvProductOfferPrice")
    currVal = 0
    number_of_product_to_add = 0

    for price in searched_product_prices:
        match = re.search(r'\d+', price.text) #convert price rs00 into plain numbers
        price_in_numbers = match.group(0)
        print(price_in_numbers)
        currVal += int(price_in_numbers)
        number_of_product_to_add += 1
        if currVal > int(req_amt_to_unlock):
            break

    print(f'{number_of_product_to_add} products requires to be added to unlock')


    for i in range(number_of_product_to_add):
        try:
            '''since everytime we add an item the screen has refreshed, and the new items which have add_btn active 
            will become the 0th instance, hence everytime we add 0th instance item'''
            add_item = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddToCart").instance(0)')))
            print(f'Adding {i+1} item...')
            add_item.click()
            time.sleep(0.75)
        except TimeoutException:
            pass

    print(f'✅ Successfully added all {number_of_product_to_add} items of {req_amt_to_unlock} amt collectively.')
    view_cart(wait)


# find the product name and its sp against it in the cart page on the product list
'''
1. find all_product_name
2. check if the find all_product_name has any name that already exists in product_name
3. if no, then add those all_product_name inside the product_name, and all_product_sp inside the product_sp
4. if yes, then skip that name and try to look that is there any new product name in all_product_name,
    and also count the skip, if we have found a product name that doesn't already exists after some skips, then add it to the product_name, 
    and then after doing that, do all_product_sp, and add product_sp after skipping the number of times we skip in all_product_name.
'''

from selenium.webdriver.remote.webdriver import WebDriver
from typing import List, Tuple

# --- GLOBAL/PERSISTENT LISTS ---
# In a real test framework, these would be class variables or passed between functions.
# We define them here for simplicity.
PRODUCT_NAMES_STORED: List[str] = []
PRODUCT_SPS_STORED: List[str] = []

# --- CONFIGURATION ---
# MAX_SCROLLS = 20  # Safety limit
NAME_LOCATOR = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="product name"]'
PRICE_LOCATOR = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="product sp"]'


def _perform_vertical_scroll(driver: WebDriver) -> None:
    """Helper function to perform a standard vertical scroll down."""
    size = driver.get_window_size()
    width = size['width']
    height = size['height']
    # Scroll from 80% down to 20% down
    start_x = width // 2
    start_y = int(height * 0.75)
    end_x = width // 2
    end_y = int(height * 0.25)

    driver.swipe(start_x, start_y, end_x, end_y, 500)
    time.sleep(1)


def collect_and_sync_product_data(driver: WebDriver) -> int:
    """
    Finds visible names/prices, checks for duplicates against the global store,
    and adds only unique data to the persistent lists (PRODUCT_NAMES_STORED, PRODUCT_SPS_STORED).

    Returns the number of NEW unique products found in this scroll cycle.
    """

    # 1. Fetch all elements currently visible on the screen
    try:
        all_name_elements = driver.find_elements(*NAME_LOCATOR)
        all_price_elements = driver.find_elements(*PRICE_LOCATOR)
    except TimeoutException:
        print("No product elements found on the current screen.")
        return 0

    if len(all_name_elements) != len(all_price_elements):
        print(f"❌ ERROR: Found {len(all_name_elements)} names but {len(all_price_elements)} prices. Cannot sync!")
        return 0

    new_products_found_in_cycle = 0

    # 2. Iterate, Filter, and Synchronize
    for i in range(len(all_name_elements)):
        current_name = all_name_elements[i].text.strip()
        current_price = all_price_elements[i].text.strip()

        # 3. Check if the name already exists in the persistent list
        if current_name in PRODUCT_NAMES_STORED:
            # 4. If yes (duplicate), skip and continue to the next item
            # The synchronization is maintained because 'i' still increases for both lists.
            continue

        # 5. If no (new product), add it to both persistent lists
        print(f"✅ Found NEW item: '{current_name}' (Price: {current_price}). Adding.")

        PRODUCT_NAMES_STORED.append(current_name)
        PRODUCT_SPS_STORED.append(current_price)
        new_products_found_in_cycle += 1

    return new_products_found_in_cycle


def scroll_and_collect_data(driver, wait, max_swipes) -> Tuple[List[str], List[str]]:
    """
    Scrolls down the screen until the end is reached, collecting all unique product data.
    """
    global PRODUCT_NAMES_STORED, PRODUCT_SPS_STORED

    # Reset the global lists for a clean run
    PRODUCT_NAMES_STORED = []
    PRODUCT_SPS_STORED = []
    previous_page_source = ""

    print("--- STARTING SCROLL AND DATA COLLECTION ---")

    for i in range(max_swipes):
        print(f"\n--- Scroll cycle {i + 1} / {max_swipes} ---")

        # 1. Collect and synchronize data on the current screen
        new_items_count = collect_and_sync_product_data(driver)
        print(f"Summary: Found {new_items_count} new items this cycle. Total unique items: {len(PRODUCT_NAMES_STORED)}")

        # 2. Check for End of Page (MUST check after collecting data, not before)
        current_page_source = driver.page_source

        try:
            wait.until(EC.presence_of_element_located(
                (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/bannerTextLayoutUnlocked"'))
            )
            print('All Products has been found!')
            break
        except TimeoutException:
            pass

        if current_page_source == previous_page_source:
            print("🛑 Reached end of the page (Page source did not change). Stopping scroll.")
            break

        previous_page_source = current_page_source

        # 3. Perform Scroll
        _perform_vertical_scroll(driver)

    print("\n--- COLLECTION FINISHED ---")
    print(f"Total unique products collected: {len(PRODUCT_NAMES_STORED)}")

    return PRODUCT_NAMES_STORED, PRODUCT_SPS_STORED
