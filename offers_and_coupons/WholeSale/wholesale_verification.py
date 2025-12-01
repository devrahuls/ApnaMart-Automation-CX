import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import re
from offers_and_coupons.WholeSale.Helpers import add_more_products_to_unlock_wh_cart, scroll_and_collect_data

def verify_vip_offer_wholesale_bottomsheet(wait):
    """
        Verifies if the Wholesale-VIP Offer Tag is visible on product.
    """

    print('Checking for Wholesale-VIP verification tag...')
    try:
        # checking the vip-offer-tag for the very first product id
        verify_tag = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/vip_offer_layout'))
        )
        print("Verification successful: VIP Offer Tag is visible.")

        verify_tag.click()  # to open the wholesale-hafta offer-tag bottomsheet
        print('WholeSale Hafta bottomsheet has opened')

        try:
            # closing the bottomsheet
            bottomsheet_close_btn = wait.until(
                EC.visibility_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Close")'))
            )
            bottomsheet_close_btn.click()
            print('WholeSale Hafta bottomsheet closed')
        except:
            print('WholeSale Hafta bottomsheet has not been found')

    except:
        print("Verification failed: VIP Offer Tag is NOT visible.")

# confirmation of name and price of the WH offer item
PRODUCT_NAME = ''
PRODUCT_SP = ''
def add_wh_item_to_cart(driver, wait):
    verify_vip_offer_wholesale_bottomsheet(wait) #verify vip-offer wholesale-bottomsheet

    first_product_tile = wait.until(
        EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/ivProduct").instance(0)'))
    )
    first_product_tile.click()
    print('clicked on the first product tile.')

    verify_vip_offer_wholesale_bottomsheet(wait) #verify vip-offer wholesale-bottomsheet

    # gather wh offer product name and wh price to confirm that offer has been successfully applied
    try:
        product_name = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/item_name'))
        )
        PRODUCT_NAME = product_name.text
    except TimeoutException:
        print('Product name NOT found')

    # TODO - When ids will get by Team
    # try:
    #     product_sp = wait.until(
    #         EC.visibility_of_element_located((AppiumBy.ID, ''))
    #     )
    #     PRODUCT_SP = product_sp.text
    # except TimeoutException:
    #     print('Product SP NOT found')
    #adding the offer product to the cart
    add_product_to_cart = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btAddBig'))
    )
    add_product_to_cart.click()

    # closing the pdp
    pdp_close_btn = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_close'))
    )
    pdp_close_btn.click()

    view_cart_btn = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/viewCart'))
    )
    view_cart_btn.click()


def verify_wh_cart_page_elements(driver, wait):
    ELEMENT_IDS = {
        "single_sku_deals": "com.apnamart.apnaconsumer:id/single_sku_deals",
        "layout_coupon_section": "com.apnamart.apnaconsumer:id/layout_coupon_section",
        "cartBillDetailsLayout": "com.apnamart.apnaconsumer:id/cartBillDetailsLayout",
        "cartCancellationAndRefundLayout": "com.apnamart.apnaconsumer:id/cartCancellationAndRefundLayout",
    }
    MANDATORY_KEYS = {
        'layout_coupon_section',
        'cartBillDetailsLayout',
        'cartCancellationAndRefundLayout'
    }
    MAX_SCROLLS = 15  # Safety limit to prevent infinite loops

    def _perform_swipe(driver) -> None:
        """Helper function to perform a scroll from 70% to 30%."""
        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        # Scroll coordinates (70% down to 30% down)
        start_x = width // 2
        start_y = int(height * 0.70)
        end_x = width // 2
        end_y = int(height * 0.30)

        driver.swipe(start_x, start_y, end_x, end_y, 500)  # 500ms duration
        # time.sleep(0.25)  # Pause for UI stabilization

    def scroll_and_verify_elements(driver, max_swipes: int = MAX_SCROLLS) -> bool:
        """
        Scrolls the screen to the end, checking for the presence of mandatory elements.
        """

        found_elements = set()
        previous_page_source = ""

        for i in range(max_swipes):
            print(f"--- Scroll cycle {i + 1} / {max_swipes} ---")

            # 1. CHECK FOR ELEMENTS ON CURRENT SCREEN
            elements_found_in_cycle = 0
            for key, resource_id in ELEMENT_IDS.items():

                # Check if we already found this element OR if the element is not mandatory
                if key in found_elements:
                    continue

                # Find elements is used for non-failing existence check
                elements = driver.find_elements(AppiumBy.ID, resource_id)

                if elements:
                    found_elements.add(key)
                    elements_found_in_cycle += 1
                    print(f"✅ FOUND: Element '{key}' located.")

            if elements_found_in_cycle > 0:
                print(f"✅ Found {elements_found_in_cycle} new element(s). Total found: {len(found_elements)}.")

            # 2. CHECK FOR END OF PAGE
            current_page_source = driver.page_source
            if current_page_source == previous_page_source:
                print("--- Reached end of the page, Stopped scrolling. ----")
                break

            previous_page_source = current_page_source

            # 3. PERFORM SCROLL
            _perform_swipe(driver)

        # 4. FINAL VERIFICATION
        # Check if the set of found elements contains all mandatory elements
        missing_elements = MANDATORY_KEYS.difference(found_elements)

        if not missing_elements:
            print("\n🎉 SUCCESS: All mandatory elements were found during scrolling.")
            return True
        else:
            print("\n❌ FAILED: The following mandatory elements were NOT found:")
            for key in missing_elements:
                print(f"   - {key} ({ELEMENT_IDS.get(key)})")
            return False
    scroll_and_verify_elements(driver, max_swipes=MAX_SCROLLS)


def locked_wh_cart_verification(driver, wait):
    # adding the WH offer item on the cart
    add_wh_item_to_cart(driver, wait)

    # verify have we unlocked the WH cart, or in normal cart
    # verify wholesale savings banner on the normal cart
    try:
        wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//android.view.View[@resource-id="wholesale savings banner"]/android.view.View'))
        )
        print("✅ Wholesale savings banner is visible on Normal Cart.")
    except TimeoutException:
        print("❌  Wholesale savings banner is NOT visible on Normal Cart.")

    # redirect to the WH cart
    try:
        wholesale_cart_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.view.View[@resource-id="Wholesale Cart"]'))
        )
        wholesale_cart_btn.click()
        print("✅ Redirected to the Wholesale Cart.")
    except TimeoutException:
        print("❌ Unable to Redirect to the Wholesale Cart.")

    # verify gift at 1 is present on wholesale cart
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/gift_badge'))
        )
        print("✅ gift at 1 is visible on Wholesale Cart.")
    except TimeoutException:
        print('Gift badge NOT visible / NOT active on Wholesale Cart.')

    # verify search btn is visible or not on the WH Cart
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/search_btn'))
        )
        print("✅ Search Button on heading is visible on Wholesale Cart.")
    except TimeoutException:
        print("❌ Search Button on heading is NOT visible on Wholesale Cart.")

    # verify WH offer primary image on heading
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/wholeSalePrimaryImage'))
        )
        print("✅ WH offer primary image on heading is visible on Wholesale Cart.")
    except TimeoutException:
        print("❌ WH offer primary image on heading is NOT visible on Wholesale Cart.")

    # verify banner text 'Add Items Worth XX price more to unlock' on heading (this wont be present in unlocked WH Cart)
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/wholeSalePrimaryImage'))
        )
        print("✅ WH offer banner text is visible on Wholesale Cart.")
    except TimeoutException:
        print("❌ WH offer banner text is NOT visible on Wholesale Cart.")

    # verify service unavailable text
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/text_service_unavailable'))
        )
        print('Service Unavailable Text Banner is Available.')
    except TimeoutException:
        print('Service Unavailable Text Banner is NOT Available.')

    # verify best deals and spd offers (if present)
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/multi_sku_deals'))
        )
        print('Best Deals Offers is present on Wholesale Cart.')
    except TimeoutException:
        print('Best Deals Offers is NOT present / NOT active on Wholesale Cart.')


    # verify cart product list
    try:
        cart_product_list = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/composeProductList'))
        )
        print('Cart Product List is visible on Wholesale Cart.')
    except TimeoutException:
        print('Cart Product List is NOT visible on Wholesale Cart.')

    # verify wholesale cart elements that present on the normal cart
    verify_wh_cart_page_elements(driver, wait)

    # verify locked_footer_text
    try:
        locked_footer_text_start = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/heading_text_locked_offer_cart_start'))
        )
        locked_footer_text_center = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/heading_text_locked_offer_cart_center'))
        )
        locked_footer_text_end = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/heading_text_locked_offer_cart_end'))
        )
        print(
            f'✅ Locked WH Cart Footer Text: {locked_footer_text_start.text, locked_footer_text_center.text, locked_footer_text_end.text} is visible on Wholesale Cart')
    except TimeoutException:
        print('❌ Locked WH Cart Footer Text is NOT available on Wholesale Cart.')

    # verify locked button on footer
    try:
        shop_more_to_unlock_btn = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/offer_cart_locked_btn'))
        )
        print('✅ Shop More To Unlock Button is Available on the Locked WH Cart Cart.')
    except TimeoutException:
        print('❌ Shop More To Unlock Button is NOT Available on the Locked WH Cart Cart.')


def unlocked_wh_cart_verification(driver, wait):
    # in order to unlock the cart first we need to add items more to unlock it

    # gather required amt to unlock this wholesale cart
    req_amt_to_unlock = wait.until(EC.presence_of_element_located(
        (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/heading_text_locked_offer_cart_center'))
    )
    if not req_amt_to_unlock.is_displayed:
        print('Cart is Unlocked')
    else:
        print(f'Cart is Locked! {req_amt_to_unlock.text} amt is required to unlock the cart.')

        # Extract only number from the ₹00
        match = re.search(r'\d+', req_amt_to_unlock.text)
        if match:
            req_amt_to_unlock_number = match.group(0)
        else:
            print("No digits found.")

        search_btn = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/search_btn'))
        )
        search_btn.click()
        add_more_products_to_unlock_wh_cart(driver, wait, req_amt_to_unlock_number)

    # verify wh unlocked cart elements
    # verify wh cart header pill
    try:
        wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Wholesale Cart Unlocked")'))
        )
        print("✅ Wholesale Cart Unlocked!")
    except TimeoutException:
        print("❌ Wholesale Cart is still Locked / Wholesale Pill at header NOT found")
    # verify wh cart header img
    try:
        wait.until(EC.presence_of_element_located(
                (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/wholeSalePrimaryImage'))
        )
        print("✅ Wholesale Cart Header Image is Available!")
    except TimeoutException:
        print("❌ Wholesale Cart Header Image is NOT Available")
    # verify wh cart header text banner
    try:
        wait.until(EC.presence_of_element_located(
                (AppiumBy.ID, 'com.apnamart.apnaconsumer:id/bannerTextLayoutUnlocked"'))
        )
        print("✅ Wholesale Cart Banner text on Header is Available!")
    except TimeoutException:
        print("❌ Wholesale Cart Banner text on Header is NOT Available")

    collected_names, collected_prices = scroll_and_collect_data(driver, 20)
    print(collected_names)
    print(collected_prices)

    for i in range(len(collected_names)):
        if collected_names[i] == PRODUCT_NAME:
            if PRODUCT_SP == collected_prices[i]:
                print('✅ Correct WH Offer Price has been Applied!')
            else:
                print('❌ Incorrect WH Offer Price has been Applied!')
        else:
            print('WH Offer Product Name NOT found!')