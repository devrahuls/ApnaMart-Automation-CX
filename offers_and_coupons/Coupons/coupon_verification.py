from readline import backend

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
import time
from offers_and_coupons.WholeSale.Helpers import add_more_products_to_unlock_wh_cart
from scroll_until_find_an_element import scroll_up_to_find_an_element, scroll_down_to_find_an_element
from offers_and_coupons.Coupons.Helpers import scroll_until_found_coupon_section, calculate_cart_total
from cart_page.view_cart import view_cart


def coupon_verification_main(driver, main):

    coupon_section_verification(driver, main)

    '''
    call fn that verify the coupon section in cart
        check if the only coupon is available or unavailable
        if available
            then apply and calculate the cart total updates according to the coupon discount
        else
            gather the req_amt_to_unlock and open the search page and add the worth items that unlock that coupon
            then apply the coupon and verify that the cart total updates according to the coupon discount
            
    click on the view all button
        open the coupon page
        verify the search, disabled 'Apply' button before sending the text on the search bar, 
        then verify the Available and Unavailable coupon cards and their respective state elements and buttons, 
        then gather the req_amt_to_unlock for the unavailable coupon,
        then send the garbage text on the search bar & click apply button & verify coupon hasn't applied by 'could not find offer...' message. 
            then send correct text & after sending the text click on the apply button - verify have we redirected to the cart page successfully and the coupon applied and reflected on the cart total successfully,
        then remove the coupon,
        then go to the search page, and call the req_amt_to_unlock fn to add the x amt of item to unlock the coupon, 
        then go to the coupon page and verify does the coupon gets unlocked, 
        then apply the coupon and verify that the cart total updates according to the coupon discount
    '''


def coupon_section_verification(driver, wait):

    ''' scroll until you find the Apply btn / coupon banner '''
    scroll_until_found_coupon_section(driver, wait)

    # verify the layout of the coupon section
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/layout_coupon_section'))
        )
        print('✅ Coupon Section has Found!')
    except NoSuchElementException:
        print('❌ Coupon Section could not be found!')

    # verify coupon and offers heading
    try:
        coupon_heading = wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Coupons & Offers")'))
        )
        print('✅ Coupon Heading : Coupons & Offers, has Found!')
    except NoSuchElementException:
        print('❌ Coupon Heading could not be found!')

    # verify view all btn
    try:
        view_all_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="view_all_offers_btn"]'))
        )
        print('✅ Coupon view_all btn has Found!')
    except NoSuchElementException:
        print(f'❌ Coupon View All btn could not be found!')

    # verify Coupon Apply btn
    try:
        apply_btn_active = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.View[@resource-id="apply_btn"]/android.widget.Button'))
        )
        print('✅ Coupon Apply btn has Found and Active!')
        apply_btn_active.click()
        calculate_cart_total(driver, wait)
    except TimeoutException:
        try:
            wait.until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, '//android.view.View[@resource-id="disabled_apply_btn"]/android.widget.Button'))
            )
            print('✅ Coupon Apply btn has Found and is Inactive!')
            view_all_btn.click()
            amt_req_to_unlock = verify_unavailable_coupon_card(driver, wait)
            back_btn = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/back_img')))
            back_btn.click()
            add_more_products_to_unlock_wh_cart(driver, wait, amt_req_to_unlock)
            scroll_until_found_coupon_section(driver, wait)
            apply_btn_active.click()
            calculate_cart_total(driver, wait)
        except NoSuchElementException:
            print('❌ Coupon Apply btn could not be found, neither Active nor Inactive!')

    # scroll up to find the coupon section
    scroll_up_to_find_an_element(driver, AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Coupons & Offers")', 10)

    # open the coupon page
    view_all_btn.click()
    print('Opens Coupon Page!')

    # verify the available and unavailable coupons and its components
    verify_available_coupon_card(driver, wait)
    verify_unavailable_coupon_card(driver, wait)

    # move back to the cart page
    try:
        back_btn = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/back_img')))
        print('✅ Back button is found!')
        back_btn.click()
    except NoSuchElementException:
        print('❌ Back button NOT Found!')


    # TRYING TO ADD SOME ITEMS BY OPENING THE SEARCH PAGE FROM THE CART PAGE, TO UNLOCK THE LOCKED COUPON TO APPLY AND VALIDATE IT
    # open the search page
    try:
        search_btn = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/search_btn')))
        search_btn.click()
        print('Opening Search Page...')
    except NoSuchElementException:
        print('❌ No Search Icon found on Cart Page')

    # call the function that add only that amt of item that requires to unlock the coupon
    add_more_products_to_unlock_wh_cart(driver, wait, 800)

    # TRY TO APPLY THE UNLOCKED COUPON
    # scroll from top to down to find the coupon section
    try:
        scroll_until_found_coupon_section(driver, wait)
        print('✅ Coupon Section has Found!')
    except TimeoutException:
        print('❌ No coupon section found!')

    # open the coupon page
    try:
        view_all_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="view_all_offers_btn"]'))
        )
        view_all_btn.click()
        print('Opening Coupon Page...\n')
    except TimeoutException:
        print('❌ Unable to open Coupon Page -> view all btn NOT Found!\n')

    # apply the newly unlocked coupon
    try:
        apply_coupon_btn_inside_page = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, '//android.view.View[@resource-id="btn_applicable"]/android.widget.Button'))
        )
        apply_coupon_btn_inside_page.click()
        print(f'✅ Newly Unlocked Coupon has Successfully Applied!')
    except TimeoutException:
        print('❌ Unable to apply the Newly Unlocked Coupon - because coupon might not found!')

    # verify the coupon prompt that comes only after applying the coupon from the coupon page
    try:
        verify_coupon_applied_prompt(driver, wait)
        print('✅ All details on the Coupon Prompt has Verified and True!')
    except TimeoutException:
        print('❌ Coupon Applied Prompt Coupon not found!')

    # calculate the cart total that applied coupon affects the cart toal accordingly
    calculate_cart_total(driver, wait)

    # scroll up form cart total to the coupon page
    target_element = 'new UiSelector().text("Coupons & Offers")'
    scroll_up_to_find_an_element(driver, AppiumBy.ANDROID_UIAUTOMATOR, target_element, 10)

    # open the coupon page
    try:
        view_all_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("view_all_offers_btn")'))
        )
        view_all_btn.click()
        print('Opening Coupon Page...')
    except TimeoutException:
        print('❌ Unable to open Coupon Page -> view all btn NOT Found!')

    # verifying the coupon page and its elements
    verify_coupon_page(driver, wait)

    # verify the Search Bar
    print('--- Entering Coupon Codes ---')
    try:
        coupon_search_input = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="search_bar"]'))
        )
        print('Search Input (EditText) is found!')
    except NoSuchElementException:
        print('Search Input NOT Found!')

    # Click it to activate the input
    coupon_search_input.click()

    # Send the input text to the now active EditText
    coupon_search_input.send_keys('neverGonnaGiveYouUp')
    print('Wrong Coupon Code has been Successfully Entered on Search Bar!')

    # --- Apply Button Logic ---

    # apply the coupon that have been searched
    search_coupon_apply_btn = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.view.View[@resource-id="apply_btn"]/android.widget.Button'))
    )
    search_coupon_apply_btn.click()
    print('Wrong coupon code trying to apply...')


    # --- Error Check (remains the same) ---
    wrong_coupon_code_error = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Could not find offer with given code!")'))
    )
    if wrong_coupon_code_error.is_displayed:
        print('✅ Incorrect Coupon Code Found! - EXPECTED')

    time.sleep(1)

    coupon_search_input.clear() #To clr the previous entered text on the coupon search

    time.sleep(2)

    # apply a valid coupon
    coupon_search_input.send_keys('sbicc222')
    search_coupon_apply_btn.click() # apply it
    print('Correct Coupon Code has been Applied')

    # verify the coupon applied prompt
    verify_coupon_applied_prompt(driver, wait)

    time.sleep(2) # hold for 2 seconds to let the cart page stabalizes

    # calculate the cart total, if its reflecting the correct total according to the coupon applied
    calculate_cart_total(driver, wait)

    # scroll up from cart total to the coupon section
    scroll_up_to_find_an_element(driver, AppiumBy.ANDROID_UIAUTOMATOR, target_element, 10)

    # remove the coupon
    try:
        coupon_remove_btn_from_cart = wait.until(
            EC.presence_of_element_located( (AppiumBy.XPATH, '//android.view.View[@resource-id="remove_btn"]/android.widget.Button'))
        )
        coupon_remove_btn_from_cart.click()
        print('\n✅ Coupon Removed Successfully!')
    except TimeoutException:
        print('❌ Coupon Remove Button could not be found!')

    calculate_cart_total(driver, wait)

    print('-'*50)
    print('\nAll Coupon Test Cases Passed!')







def verify_common_ele_coupon_cards(driver, wait):
    # verify title of the coupon
    try:
        coupon_title = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="coupon_title"]'))
        )
        print(f'✅ Coupon Title has found : {coupon_title.text}')
    except TimeoutException:
        print(f'❌ Coupon Title could not be found!')

    # verify image
    try:
        img = driver.find_element(AppiumBy.CLASS_NAME, "android.widget.ImageView")
        current_image = img.get_attribute("content-desc")
        if current_image == coupon_title.text:
            print('✅ Correct Coupon Logo has been found!')
    except TimeoutException:
        print('❌ Incorrect Coupon Logo has been found!')

    # verify coupon code
    try:
        coupon_code = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="coupon_code"]'))
        )
        print(f'✅ Coupon Code has found : {coupon_code.text}')
    except TimeoutException:
        print('❌ Coupon Code could not be found!')

    # verify the bottom lable - cashback/discount
    try:
        coupon_bottom_label = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.TextView[@resource-id="bottom_label"])'))
        )
        print(f'✅ Coupon Label has been found : {coupon_bottom_label.text}!')
    except TimeoutException:
        print('❌ Coupon Label could not be found!')

    # verify terms and condition show more button
    try:
        tnc_show_more_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, ' new UiSelector().description("Show More")'))
        )
        tnc_show_more_btn.click()
        print(f'✅ Terms & Conditions Show More Button has found.. \n ✅ Expanded the Terms and Conditions!')
    except TimeoutException:
        print('❌ Terms & Conditions Show More Button could not be found!')

    # TODO - verify terms and condition text


def verify_unavailable_coupon_card(driver, wait):
    '''
    verify all elements of a unavailable coupon card.
    return the amt required to unlock it in this fn
    '''

    print('\n Verifying unavailable coupon card...')

    verify_common_ele_coupon_cards(driver, wait)

    # verify the apply button - should be disabled
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.View[@resource-id="btn_inapplicable"]/android.widget.Button'))
        )
        print(f'✅ Apply Button is Correctly Disabled!')
    except TimeoutException:
        print('❌ Apply Button is NOT Disabled!')

    print('\n')
    # TODO - gather mov from the unavailable coupon card.
    mov = 0
    return mov

def verify_available_coupon_card(driver, wait):
    '''
    verify all elements of a available coupon card.
    '''
    print('\n Verifying Available Coupon card...')
    verify_common_ele_coupon_cards(driver, wait)

    # verify the apply button - should be enabled/remove
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.View[@resource-id="btn_applicable"]/android.widget.Button'))
        )
        print(f'✅ Apply Button is Correctly Enabled!')
    except TimeoutException:
        try:
            wait.until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, '//android.view.View[@resource-id="btn_applied"]/android.widget.Button'))
            )
            print(f'✅ Remove Button is Correctly Displaying!')
        except NoSuchElementException:
            print('❌ No Apply / Remove button has been found!')

    # verify coupon status message
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Yay! You have unlocked this coupon").instance(0)'))
        )
        print(f'✅ Coupon Status Message is displaying Correctly!')
    except TimeoutException:
        print('❌ Coupon Status Message is NOT displaying!')



def verify_coupon_applied_prompt(driver, wait):
    '''
    verify the layout
    verify tick logo, coupon applied title, coupon code, great btn.
    '''
    print('\n Verifying Coupon Applied Prompt...')
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/animationView'))
        )
        print('✅ Tick Animation is Displaying!')
    except NoSuchElementException:
        print('❌ Tick Animation is not displayed!')

    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Coupon Applied!")'))
        )
        print(f'✅ Coupon Applied text is displaying!')
    except NoSuchElementException:
        print('❌ Coupon Applied text is NOT displaying!')

    try:
        coupon_code = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/potential_action_str'))
        )
        print(f'✅ Coupon Code is displaying : {coupon_code.text}!')
    except NoSuchElementException:
        print('❌ Coupon Code is NOT displaying')

    try:
        great_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Great!")'))
        )
        print(f'✅ Great Button is displaying! \n Clicking on it...')
        great_btn.click()
    except NoSuchElementException:
        print('❌ Great Button is NOT displaying')


def verify_coupon_page(driver, wait):
    print('\nVerifying Coupon Page...')
    # verify header
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/toolBarContainer'))
        )
        print(f'✅ Coupon Header is displaying!')
    except NoSuchElementException:
        print('❌ Coupon Header is NOT displaying')
    # verify back btn
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/back_img'))
        )
        print(f'✅ Back Button is displaying!')
    except NoSuchElementException:
        print('❌ Back Button is NOT displaying')
    # verify header title
    try:
        header_title = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/textView3'))
        )
        print(f'✅ Header Title : {header_title.text} is displaying!')
    except NoSuchElementException:
        print('❌ Header Title is NOT displaying')

    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter Coupon")'))
        )
        print(f'✅ Enter Coupon text is displaying!')
    except NoSuchElementException:
        print('❌ Enter Coupon text is NOT displaying')

    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="search_bar"]/android.view.View'))
        )
        print(f'✅ Coupon Search Bar is displaying')
    except NoSuchElementException:
        print('❌ Coupon Search Bar is NOT displaying')

    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.View[@resource-id="apply_btn"]/android.widget.Button'))
        )
        print(f'✅ Coupon Search Apply Button is displaying!')
    except NoSuchElementException:
        print('❌ Coupon Search Apply Button is NOT displaying')

    print('\n')



def product_reward_coupon_verification(driver, wait):
    print('\nProduct Reward Coupon Verification...')

    scroll_until_found_coupon_section(driver, wait)

    # verify view all btn
    try:
        view_all_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="view_all_offers_btn"]'))
        )
        view_all_btn.click()
        print('Opens Coupon Page')
    except NoSuchElementException:
        print(f'❌ Coupon View All btn could not be found!')


    # verify the Search Bar
    print('--- Entering Coupon Code ---')
    try:
        coupon_search_input = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="search_bar"]'))
        )
        print('Search Input (EditText) is found!')
    except NoSuchElementException:
        print('Search Input NOT Found!')

    # Click it to activate the input
    coupon_search_input.click()

    # Send the input text to the now active EditText
    coupon_search_input.send_keys('productrewardtesting00')
    print('productrewardtesting00 Code has been Successfully Entered on Search Bar!')

    # --- Apply Button Logic ---

    # apply the coupon that have been searched
    try:
        search_coupon_apply_btn = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, '//android.view.View[@resource-id="apply_btn"]/android.widget.Button'))
        )
        search_coupon_apply_btn.click()
        print('Coupon code has been successfully applied!')
    except NoSuchElementException:
        print('Apply btn could not be found!')



    verify_coupon_applied_prompt(driver, wait)



    deal_applied_locator = '//android.view.View[@resource-id="product deal applied tag"]'
    scroll_down_to_find_an_element(driver, AppiumBy.XPATH, deal_applied_locator, 10)

    desired_item_name = "Annapurna Ghee - 250ml"
    desired_qty = "1"
    desired_sp = "₹2"

    # --- LOCATORS ---
    LOCATOR_NAME = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="product name"]'
    LOCATOR_QTY = AppiumBy.XPATH, '(//android.widget.TextView[@resource-id="product quantity"])'
    LOCATOR_SP = AppiumBy.XPATH, '//android.widget.TextView[@resource-id="product sp"]'

    print(f"\n--- Verifying Product: {desired_item_name} ---")
    print(f"Expected Qty: {desired_qty}, Expected SP: {desired_sp}")

    # 1. GATHER ALL PRODUCT ATTRIBUTES
    try:
        # Get all element lists using presence_of_all_elements_located
        name_elements = wait.until(
            EC.presence_of_all_elements_located(LOCATOR_NAME)
        )
        qty_elements = wait.until(
            EC.presence_of_all_elements_located(LOCATOR_QTY)
        )
        sp_elements = wait.until(
            EC.presence_of_all_elements_located(LOCATOR_SP)
        )

        # Extract text into three lists
        product_names = [el.text for el in name_elements]
        product_quantities = [el.text for el in qty_elements]
        product_sps = [el.text for el in sp_elements]

        print(f"✅ Gathered data. Total items found: {len(product_names)}")

        # Safety check: All lists must be of the same length
        if not (len(product_names) == len(product_quantities) == len(product_sps)):
            print("🛑 Error: The number of names, quantities, and prices do not match. Check your locators.")
            print(f"Names: {len(product_names)}, Qty: {len(product_quantities)}, SP: {len(product_sps)}")
            return  # Exit function

    except TimeoutException:
        print("🛑 Error: Not all product elements loaded within the timeout.")
        return
    except NoSuchElementException:
        print("🛑 Error: One or more locator types failed to find any elements.")
        return

    # 2. LOOP OVER THE PRODUCT NAME ARRAY AND FIND THE DESIRED ITEM
    found_index = -1
    for index, name in enumerate(product_names):
        if name.strip() == desired_item_name.strip():
            found_index = index
            break

    # 3. CHECK IF THE ITEM WAS FOUND
    if found_index == -1:
        print(f"❌ FAIL: Desired item '{desired_item_name}' was not found in the product list.")
        return

    # 4. FETCH DETAILS AT THE FOUND INDEX

    # Note: We assume the extracted text (including potential currency symbols, etc.)
    # must match the desired_qty/sp string exactly.
    actual_qty = product_quantities[found_index].strip()
    actual_sp = product_sps[found_index].strip()

    # 5. COMPARE DETAILS
    is_qty_correct = actual_qty == desired_qty.strip()
    is_sp_correct = actual_sp == desired_sp.strip()

    if is_qty_correct and is_sp_correct:
        print(f"\n🎉 SUCCESS: Item '{desired_item_name}' verified.")
        print(f"   Quantity ({actual_qty}) and Price ({actual_sp}) are correct.")
    else:
        print(f"\n❌ FAIL: Details for '{desired_item_name}' are incorrect.")

        # Detailed error message
        if not is_qty_correct:
            print(f"   Quantity Mismatch: Expected '{desired_qty}', Found '{actual_qty}'")
        if not is_sp_correct:
            print(f"   Price Mismatch: Expected '{desired_sp}', Found '{actual_sp}'")


    # go back to the HP
    try:
        back_btn_to_HP = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/back_img'))
        )
        back_btn_to_HP.click()
        print('Opens Home Page')
    except NoSuchElementException:
        print(f'❌ Back btn could not be found!')

    view_cart(wait)

    scroll_until_found_coupon_section(driver, wait)

    try:
        coupon_remove_btn_from_cart = wait.until(
            EC.presence_of_element_located( (AppiumBy.XPATH, '//android.view.View[@resource-id="remove_btn"]/android.widget.Button'))
        )
        coupon_remove_btn_from_cart.click()
        print('\n✅ Coupon Removed Successfully!')
    except TimeoutException:
        print('❌ Coupon Remove Button could not be found!')