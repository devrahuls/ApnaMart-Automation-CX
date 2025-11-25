from logging import exception
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import re
from cart_page.view_cart import view_cart
from search_and_browse.search_and_add_to_cart_flow import search_and_add_to_cart_flow
from offers_and_coupons.Best_Deals.best_deals_application import verify_offer_price_qty_inside_carts


def best_deals_page_verification(driver, wait):
    print('Verifying the elements and cards on the Best Deals page...')
    try:
        page_heading = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/textView3'))
        )
        print(f'✅ Page Heading: {page_heading.text} is available')
    except Exception as e:
        print(f'❌ Page Heading: Best Deals is NOT available')


    # --- Verify The Elements That Are Present In Both Lock And Unlocked Offers ---
    # verifying image of the offer card
    try:
        offer_img = wait.until(
            EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/offer_image_view").instance(0)'))
        )
        print(f'✅ Offer Image is available')
    except Exception as e:
        print(f'❌ Offer Image is NOT available')

    # verify the offer quantity and the offer price
    try:
        offer_price = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_price"))
        )
        print(f'✅ Offer Price with the: {offer_price.text}, text is available')
    except Exception as e:
        print(f'❌ Offer Price is NOT available')
    try:
        offer_qty = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_quantity"))
        )
        print(f'✅ Offer Qty with the: {offer_qty.text}, text is available')
    except Exception as e:
        print(f'⚠️ Offer Qty is NOT available OR only 1 quantity is the max_redeem for the offer item')

    # verify the title of the offer card
    try:
        offer_title = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_product_name"))
        )
        print(f'✅ Offer Title with the: {offer_title.text}, text is available')
    except Exception as e:
        print(f'❌ Offer Title is NOT available')

    # verify the sub-title of the offer card
    try:
        offer_sub_title = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_product_details"))
        )
        print(f'✅ Offer Sub-Title with the: {offer_sub_title.text}, text is available')
    except Exception as e:
        print(f'❌ Offer Sub-Title is NOT available')


    #Verifying Locked Deals
    locked_deals_btn = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btn_add_products"))
    )
    if locked_deals_btn.text == "Locked":
        print("Locked Offer Found!")
        print('--- verifying the elements on the Locked offer card ---')
        # verify mov
        try:
            subtitle = wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_subtitle"))
            )
            print(f'✅ Locked subtitle text: {subtitle.text} is available')
        except NoSuchElementException:
            print('❌ Locked Subtitle text is NOT available')

        # verify progress bar
        try:
            progress_bar = wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/progress_offer"))
            )
            print(f'✅ Progress Bar with text: {progress_bar.text} is available')
        except NoSuchElementException:
            print('❌ Progress Bar is NOT available')

        # opens the bottomsheet of the lcoked deals and start to verify
        locked_deals_btn.click()
        verify_locked_bestdeal_bottomsheet(wait)
    else:
        print('❌ No Locked offers is present OR Locked button was NOT present')

    # now try to unlock all the offers
    # add_more_products_to_unlock(wait)

    #Verifying OOS Deals
    if locked_deals_btn.text == "SOLD":
        # verify mov
        try:
            subtitle = wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_subtitle"))
            )
            print(f'✅ Locked subtitle text: {subtitle.text} is available')
        except NoSuchElementException:
            print('❌ Subtitle text is NOT available')

        # verify progress bar
        try:
            progress_bar = wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/progress_offer"))
            )
            print(f'✅ Progress Bar with text: {progress_bar.text} is available')
        except NoSuchElementException:
            print('❌ Progress Bar is NOT available')

        # verify OOS watermark
        try:
            wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/iv_sold_out"))
            )
            print(f'✅ OOS WaterMark above the img is available')
        except NoSuchElementException:
            print('❌ OOS WaterMark above the img is NOT available')

        # opens the bottomsheet of the lcoked deals and start to verify
        locked_deals_btn.click()
        verify_oos_bestdeal_bottomsheet(wait)
    else:
        print('--- No OOS offer is present OR no OOS button was present ---')

    #Verifying Unlocked Deals
    try:
        choose_items_btn = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btn_choose_items"))
        )

        if choose_items_btn.is_displayed:
            print(f'✅ Unlocked Offer is available')
            choose_items_btn.click()
            verify_unlocked_bestdeals_bottomsheet_verification(driver, wait)
        else:
            print('No unlocked offer present')

            # add more products only when the item is not OOS
            add_more_products_to_unlock(wait)

    except Exception as e:
        print('❌ No offers has listed here, despite having more than one active offers')
    #Find that if there is any Locked Deals available




    # verify locked deals
        # verify oos, verify locked - and its components
    # verify unlocked deals and its components

def offer_bottomsheet_common_elements_verification(wait):
    print('--- Opening the Monthly Gift Bottomsheet ---')

    # verifying the header img of the offer
    try:
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/imageSlider"))
        )
        print('✅ Header image is available')
    except TimeoutException:
        print('❌ Header image is NOT available')
        pass

    # verifying the header title
    try:
        header_title = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_title"))
        )
        print(f'✅ Header Title is available with : {header_title.text}')
    except NoSuchElementException:
        print('❌ Header Title is NOT available')

    # verify the subtitle
    try:
        header_subtitle = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_subtitle"))
        )
        print(f'✅ Header Subtitle is available with : {header_subtitle.text}')
    except NoSuchElementException:
        print('❌ Header Subtitle is NOT available')

    # Offered Quantity
    try:
        offered_qty = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_gift_quantity"))
        )
        print(f'✅ Offered Qty is available with : {offered_qty.text}')
    except NoSuchElementException:
        print('--- Offered qty is NOT available OR only 1 quantity is the max_redeem for the offer item ---')

    # Offered Price
    try:
        offered_price = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tvProductSellingPrice"))
        )
        print('✅ Offered Price is available')
    except NoSuchElementException:
        print('❌ Offered Price is NOT available')


def get_product_names_from_bottomsheet(driver, wait):
    """Gathers all product names listed inside the bottomsheet."""

    PRODUCT_NAME_ID = "com.apnamart.apnaconsumer:id/productName"
    product_names_list = []

    try:
        # Find all matching elements using the base ID
        product_elements = driver.find_elements(AppiumBy.ID, PRODUCT_NAME_ID)

        for element in product_elements:
            name = element.text
            if name:
                product_names_list.append(name)

        return product_names_list

    except Exception as e:
        print(f"❌ Error gathering product names: {e}")
        return []



# Verification of the Unlocked Best Deals Bottomsheet elements
def verify_unlocked_bestdeals_bottomsheet_verification(driver, wait):

    # verify the header img, header title, subtitle, offer-item qty, offer-item price
    offer_bottomsheet_common_elements_verification(wait)


    # If the offer is locked then search for products and add it to the cart to reach MOV
    offer_item_add_btn = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btnAddBig"))
    )
    # If the Offer is Locked
    while offer_item_add_btn.text == "Locked":
        print("--- Offer is currently locked, please add more items to get unlocked ----")
        add_more_products_to_unlock(wait)

    # Add to cart the offer items according to the availabiltiy
    short_wait = WebDriverWait(driver, 2)
    # ADD THE OFFER ITEMS IN THE CART
    try:
        # 1. Get the title text
        title_element = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_subtitle"))
        )
        title_text = title_element.text
        # 2. Extract the number from the text
        match = re.search(r'\d+', title_text)  # Finds one or more digits

        if not match:
            print(f"❌ FAILED: Could not find any number in the text: '{title_text}'")
            return

        goal_items_to_add = int(match.group(0))
        if goal_items_to_add == 0:
            print("ℹ️ Title says 0 items to add. Nothing to do.")
            return

        print(f"--- GOAL: Add {goal_items_to_add} item(s) ---")

    except TimeoutException:
        print("❌ FAILED: Could not find the title element 'sub-title'. Test cannot continue.")
        raise  # Fail the test

        # --- 2. Try to add 'n' items ---
    items_added_successfully = 0

    if goal_items_to_add == 1:
        try:
            item_add_to_cart = short_wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btnAddBig'))
            )
            item_add_to_cart.click()
            items_added_successfully += 1
            print(f"  ✅ Clicked item. (Total added: {items_added_successfully})")
        except TimeoutException:
            print("❌ FAILED : Could not find the Add button")

    else:
        for i in range(goal_items_to_add):

            item_selector = f'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btnAddBig").instance({i})'
            print(f"Attempting to add item at instance({i})...")

            try:
                # Use the short_wait here
                item_add_to_cart = short_wait.until(
                    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, item_selector))
                )

                item_add_to_cart.click()
                items_added_successfully += 1
                print(f"  ✅ Clicked item. (Total added: {items_added_successfully})")

            except TimeoutException:
                # This means btAddBig.instance(i) was not found
                print(f"  ❌ 'btAddBig.instance({i})' not found or not clickable.")
                print("  Stopping add-to-cart loop.")
                break  # Stop the loop

    # --- GATHER PRODUCT NAMES ---
    all_product_names = get_product_names_from_bottomsheet(driver, wait)
    print("\n📦 Captured Products:", all_product_names)

    # --- 3. Final Report ---
    print("\n--- Summary ---")

    if items_added_successfully == goal_items_to_add:
        # This is the "good to go" case
        print(f"✅ Successfully added all {goal_items_to_add} item(s).")
    # adding the offer item by pressing the confirm button inside the best deals bottomsheet
    else:
        # "otherwise try to find oos button"
        print(f"ℹ️ Added {items_added_successfully} out of {goal_items_to_add} items.")

        try:
            # Check for *any* OOS buttons on the page
            oos_buttons = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/btNotifyMe")

            if oos_buttons.is_displayed:
                # "if you have found then just print..."
                print(f"  REPORT: Could only add {items_added_successfully} item(s). The rest are Out of Stock.")
            else:
                print("  REPORT: Failed to add all items, but no OOS buttons were found either.")

        except NoSuchElementException:
            print("  REPORT: Failed to add all items, and no OOS buttons were found.")


    # adding the offer item by pressing the confirm button inside the best deals bottomsheet
    try:
        confirm_btn = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btn_add_products"))
        )
        confirm_btn.click()
        print('Offer item(s) has successfully Added to Cart!')

        # verify after confirming the offer item are we successfully redirected to the cart page or not
        try:
            wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/toolBarContainer"))
            )
            try:
                print('I am trying...')
                cart_product_elements = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/product name")
                for cart_element in cart_product_elements:
                    cart_name = cart_element.text.strip()
                    print(cart_name)
            except TimeoutException:
                print("  REPORT: Failed to find product name on the cart bhai.")

            print('Successfully Redirected to the Cart Page!')
            # verify_offer_price_qty_inside_carts(driver, wait, all_product_names, items_added_successfully)
        except TimeoutException as e:
            print('Couldnt Redirected to the Cart Page!')
    except NoSuchElementException:
        print('Confirm Button could not found so Offer item cant be Added to Cart')


def verify_locked_bestdeal_bottomsheet(wait):

    # verify the header img, header title, subtitle, offer-item qty, offer-item price
    offer_bottomsheet_common_elements_verification(wait)

    # verify the progress bar
    try:
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/progress_offer"))
        )
        print('Progress Offer Bar is available')
    except TimeoutException:
        print('Progress Offer Bar is NOT available')

    # verify the Locked button
    try:
        locked_btn = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btnAddBig"))
        )
        if locked_btn.text == 'Locked':
            print('Button with Locked text is available')
        else:
            print('Button with Locked text is not available')
    except TimeoutException:
        print('Locked Button could not be found')

    # close the bottomsheet
    try:
        close_btn = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/close_btn"))
        )
        close_btn.click()
        print('Offer Bottomsheet has been closed')
    except TimeoutException:
        print('Offer Bottomsheet could not be closed')


def verify_oos_bestdeal_bottomsheet(wait):

    # verify the header img, header title, subtitle, offer-item qty, offer-item price
    offer_bottomsheet_common_elements_verification(wait)

    # verify the Locked button
    try:
        oos_btn = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btNotifyMe"))
        )
        if oos_btn.text == 'Notify':
            print('Button with Notify text is available')
        else:
            print('Button with Notify text is not available')
    except TimeoutException:
        print('OOS Button could not be found')


    # verify OOS watermark above the product img
    try:
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/iv_sold_out"))
        )
        print('SOLD OUT Watermark above item-img has been found')
    except TimeoutException:
        print('SOLD OUT Watermark above item-img couldnt be found')

    # close the bottomsheet
    try:
        close_btn = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/close_btn"))
        )
        close_btn.click()
        print('Offer Bottomsheet has been closed')
    except TimeoutException:
        print('Offer Bottomsheet could not be closed')



def add_more_products_to_unlock(wait):

    #check if are we inside the Best Deals page
    page_heading = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/textView3'))
    )
    #if inside best deals page then go back
    if page_heading.text == "Best Deals":
        best_deals_page_back_btn = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/back_img'))
        )
        best_deals_page_back_btn.click()

    # otherwise go back to straight to the homepage
    cart_page_back_btn = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/back_img'))
    )
    cart_page_back_btn.click()
    search_and_add_to_cart_flow(wait, "shampoo")
    view_cart(wait)


def offer_card_bottomsheet_from_cart(driver, wait):
    """
    Verifies the offer state (Unlocked, Locked, OOS) based on the text
    of the single control button (btnAddBig) and calls the respective verification function.
    """

    CONTROL_BUTTON_ID = "com.apnamart.apnaconsumer:id/btnAddBig"

    print("--- Verifying Offer State Inside Bottomsheet ---")

    try:
        # We wait until the main control button of the bottomsheet is visible.
        # This confirms the bottomsheet has loaded its content.
        control_btn = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, CONTROL_BUTTON_ID))
        )

        # Get the text from the button and convert to uppercase for robust comparison
        button_text = control_btn.text.upper()
        print(f"ℹ️ Control button text found: '{button_text}'")

        if button_text == "ADD":
            # --- State 1: UNLOCKED OFFER ---
            print("✅ STATE: Offer is UNLOCKED (Text: ADD).")
            # Usually, if it says 'Add', we should click it and then verify the success.
            # control_btn.click() # Uncomment if clicking is part of your verification flow
            verify_unlocked_bestdeals_bottomsheet_verification(driver, wait)

        elif button_text == "LOCKED":
            # --- State 2: LOCKED OFFER ---
            print("✅ STATE: Offer is LOCKED.")
            verify_locked_bestdeal_bottomsheet(wait)
            add_more_products_to_unlock(wait)
            offer_card = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/sku_deals_cardview'))
            )
            offer_card.click()
            offer_card_bottomsheet_from_cart(driver, wait)#recursion bawa

        elif button_text == "SOLD":
            # --- State 3: OOS OFFER ---
            print("✅ STATE: Offer is SOLD OUT (OOS).")
            verify_oos_bestdeal_bottomsheet(wait)

        else:
            # --- State 4: UNEXPECTED TEXT ---
            print(f"❌ FAILED: Found control button, but text was '{button_text}'.")
            raise AssertionError(f"Unexpected control button text in bottomsheet: {button_text}")

    except TimeoutException:
        # If the control button is never found, the bottomsheet failed to load
        print("\n" + "=" * 30)
        print("❌ FAILED: FINAL REPORT")
        print(f"   -> Could not find control button '{CONTROL_BUTTON_ID}'.")
        print("   -> Bottomsheet content failed to load within timeout.")
        print("=" * 30 + "\n")
        raise AssertionError("Bottomsheet failed to load or has no state indicator.")

# Main function to run all the flow
def best_deals_validate_main(driver, wait):

    try:
        # --- STATE 1: Multiple Offers ---
        print("Checking for 'View All' button...")
        view_all_btn = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/bt_view_all'))
        )

        print('✅ "View All" button is present (Multiple offers).')
        view_all_btn.click()
        print('Opening the Best Deals Page...')

        best_deals_page_verification(driver, wait)

    except TimeoutException:
        # --- STATE 2: Single Offer ---
        # This block runs ONLY if the 'View All' button was NOT found.
        print("ℹ️ 'View All' button NOT found (Assuming single offer).")

        try:
            # Now, we *expect* the single offer card to be clickable
            offer_card = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/sku_deals_cardview'))
            )
            offer_card.click()
            print('✅ Opening the Offer Bottomsheet')

            # if view all button does not found, means we have only one offer to check, verify, and apply.
            try:
                offer_card_bottomsheet_from_cart(driver, wait)
            except Exception as e:
                print(f'❌ Error inside Single Offer verification: {e}')
                raise e  # Re-raise to fail the test if verification failed


        except TimeoutException:
            # This is a critical failure: *neither* element was found.
            print('❌ FAILED: UI is in an unexpected state.')
            print("   -> 'View All' button was not found,")
            print("   -> AND 'sku_deals_cardview' was also not found.")
            # Fail the test
            raise AssertionError("Offer state is invalid: Neither 'View All' nor 'Offer Card' was found.")

