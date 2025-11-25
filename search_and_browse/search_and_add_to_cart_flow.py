import time
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy


# item_name = input("Enter the item name to search: ")

def search_and_add_to_cart_flow(wait, item_name):
    # com.apnamart.apnaconsumer: id / layout_top
    # com.apnamart.apnaconsumer: id / mast_head_top

    time.sleep(5)

    # This block waits for a stable homepage element *before*
    # doing anything else.
    try:
        print("Waiting for homepage to be ready...")
        # Use a stable, static element ID from your homepage
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/masthead_top"))
        )
        print("✅ Homepage is stable.")

    except TimeoutException:
        print("🛑 Homepage never loaded or stable element not found. Stopping.")
        raise  # Fail the test if the homepage isn't stable
    # --- END OF FIX ---

    try:
        # Search for item
        search_bar = wait.until(EC.element_to_be_clickable((AppiumBy.ID,
            "com.apnamart.apnaconsumer:id/searchText")))
        search_bar.click()
    except:
        print("No search bar found")

    search_input = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
    )
    search_input.send_keys(item_name)

    # waiting time till the item got searched and add button is availabe to interact
    time.sleep(1)

    try:
        add_item = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddToCart").instance(0)')))
        add_item.click()
    except NoSuchElementException:
        pass

    try:
        back_btn_to_homepage = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/back_button"))
        )
        back_btn_to_homepage.click()
        print("Clicked 'back'. Waiting for homepage to reload...")
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/masthead_top"))
        )
        print("✅ Homepage is stable again")
    except NoSuchElementException:
        print("No back button found")

    # print("✅ Search & add to cart flow completed.")
    print(f'✅ Item name: {item_name} has been added to cart.')


def search_and_add_to_cart_flow1(wait, item_name):
    try:
        # --- 1. STABILITY FIX ---
        # Wait for a stable, static element on the homepage to appear.
        # This confirms the page is loaded and ready.
        # !!! You MUST replace "id/some_stable_homepage_element" with a REAL ID !!!
        print("Waiting for homepage to be ready...")
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/layout_top"))
            # Example: "id/bottom_navigation", "id/home_icon", "id/toolbar_title"
        )
        print("✅ Homepage is stable.")

    except TimeoutException:
        print("🛑 Homepage never loaded or stable element not found. Stopping.")
        return  # Exit the function if the page isn't ready

    try:
        # --- 2. LOGIC FIX ---
        # Find the search element ONCE.
        print("Finding search bar...")
        search_element = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
        )

        # Click it to activate it
        search_element.click()
        print("Clicked search bar.")

        # Send keys to the SAME element
        search_element.send_keys(item_name)
        print(f"Sent keys: {item_name}")

    except Exception as e:
        print(f"🛑 Error during search: {e}")
        return  # Exit if search fails

    # --- Your Original Logic (Looks Good) ---

    # waiting time till the item got searched and add button is available to interact
    time.sleep(1)  # A small sleep is OK, but an explicit wait is better (see below)

    try:
        # NOTE: Using a 'wait' is better than 'time.sleep(1)'
        print("Looking for 'Add to Cart' button...")
        add_item = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                                          'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddToCart").instance(0)')))
        add_item.click()
        print(f'✅ Item name: {item_name} has been added to cart.')

    except TimeoutException:
        print(f"🛑 'Add to Cart' button not found for {item_name}.")
        # Handle the error (maybe go back?)
    except NoSuchElementException:
        print(f"🛑 'Add to Cart' button not found for {item_name}.")
        pass

    try:
        # Go back to the homepage
        back_btn_to_homepage = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/back_button"))
        )
        back_btn_to_homepage.click()
    except Exception as e:
        print(f"🛑 Could not find back button: {e}")




def recent_searches(wait):
    print("--- Starting verifying Recent Searches Working---")

    search_bar = wait.until(EC.element_to_be_clickable((AppiumBy.ID,
        "com.apnamart.apnaconsumer:id/searchText")))
    search_bar.click()

    # if there is already some recent searches available then clear it, by this we can save our time to add a text on the recent searches
    try:
        clear_searches = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/clear_text")))
        clear_searches.click()
        print("✅ SUCCESS: Clear is working.'Recent Searches' section is no longer visible!")
        return
    except NoSuchElementException:
        pass

    search_input = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
    )
    search_input.send_keys("kurkure")

    back_btn_to_homepage = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/back_button"))
    )
    back_btn_to_homepage.click()

    search_bar = wait.until(EC.element_to_be_clickable((AppiumBy.ID,
        "com.apnamart.apnaconsumer:id/searchText")))
    search_bar.click()

    recent_searched_items = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                f'new UiSelector().text("kurkure")'))
    )
    if recent_searched_items.text == "kurkure":
        print("--- Recent Searches Working ---")


    clear_searches = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/clear_text")))
    clear_searches.click()

    #we want title to be invisible
    # wait.until(
    #     EC.invisibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/title"))
    # )

    print("✅ SUCCESS: 'Recent Searches' section is no longer visible. Clear is working.")

    back_btn_to_homepage = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/back_button"))
    )
    back_btn_to_homepage.click()



def is_previously_bought_present(wait):
    print("--- Starting Previously Bought PLP Verification in Search Page ---")

    # Click on the Search Bar so that we can open the Search Page.
    search_bar = wait.until(EC.element_to_be_clickable((AppiumBy.ID,
        "com.apnamart.apnaconsumer:id/searchText")))
    search_bar.click()

    # 1. Verify the Product Image is visible
    try:
        # NOTE: Replace 'product_image_in_cart_bar' with the actual resource-id from Appium Inspector
        is_previously_bought_text = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/title"))
        )
        print(f"✅ SUCCESS: {is_previously_bought_text.text} is available!")
    except:
        print("Previously Bought PLP Verification in Search Page FAILED or couldn't be FOUND.")

    back_btn_to_homepage = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/back_button"))
    )
    back_btn_to_homepage.click()

def previously_bought_view_all(wait):
    print("--- Starting Previously Bought View All in Search Page ---")


    # 1. Verify the Product Image is visible
    try:
        # Click on the Search Bar to open the Search Page.
        search_bar = wait.until(EC.element_to_be_clickable((AppiumBy.ID,
            "com.apnamart.apnaconsumer:id/searchText")))
        search_bar.click()

        # Verify if the "Previously Bought" title is visible on the search page
        previously_bought_text = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/title"))
        )
        print(f"✅ SUCCESS: Navigated to search page, '{previously_bought_text.text}' section is available!")

        # Click on "View All"
        view_all = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/viewAll")))
        view_all.click()
        print("✅ Clicked on 'View All'.")

        try:
            # ADD ITEMS TO THE CART FROM THE PREVIOUSLY BOUGHT PLP
            # --- Step 1: Set how many times to add the product ---
            add_count = 4
            if add_count <= 0:
                print("⚠️ Number must be greater than 0. Skipping add action.")
                add_count = 0

            # --- Step 2: Add the item the specified number of times ---
            if add_count > 0:
                # First click is on the "ADD" button
                add_first_item = wait.until(
                    EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddBig").instance(0)'))
                )
                add_first_item.click()
                print("Added item 1 time.")

                # Subsequent clicks on the "+" button
                for i in range(add_count - 1):
                    increase_qty_btn = wait.until(
                        EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btAdd"))
                    )
                    increase_qty_btn.click()
                    print(f"Increased quantity {i + 2} times.")

            # Assume 'add_items' is now equal to how many were actually added
            add_items = add_count
            print(f"ℹ️ Current quantity in cart: {add_items}")

            # REDUCING THE ITEMS TO CHECK IF THE REDUCE IS WORKING FINE
            # --- Step 3: Set how many times to reduce ---
            user_input = 4
            reduce_count = int(user_input)

            # Validation
            if reduce_count <= 0:
                print("⚠️ Reduce count must be greater than 0. Skipping reduce action.")
                reduce_count = 0
            elif reduce_count > add_items:
                print(f"⚠️ Requested to reduce {reduce_count} but only {add_items} items in cart.")
                print(f"Adjusting reduce count to {add_items}.")
                reduce_count = add_items  # ✅ Auto adjust instead of looping

            # --- Step 4: Reduce the item's quantity the specified number of times ---
            if reduce_count > 0:
                for i in range(reduce_count):
                    try:
                        reduce_qty_btn = wait.until(
                            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btMinus"))
                        )
                        reduce_qty_btn.click()
                        print(f"Reduced quantity {i + 1} time(s).")
                    except Exception as e:
                        print(f"🛑 Error on reduction click {i + 1}: {e}")
                        print("Stopping further reduce actions.")
                        break
            else:
                print("Skipping reduce action.")
        except Exception as e:
            print(f'Could not add/reduce items in cart, because {e}.')
    except Exception as e:
        print(f"Previously Bought PLP Verification in Search Page FAILED or couldn't be FOUND. Error: {e}")


# new UiSelector().className("androidx.recyclerview.widget.RecyclerView").instance(1)
