from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def best_deals_verification(wait):

    # verify the whole multi sku deals component
    try:
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/multi_sku_deals"))
        )
        print("✅ Multi SKU Deals / Best Deals component is visible.")
    except TimeoutException:
        print("❌ Multi SKU Deals / Best Deals component is NOT visible.")

    # verify the offer heading
    try:
        best_deals = wait.until(
            EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Best Deals")'))
        )
        print(f'✅ {best_deals.text} offer heading is available')
    except NoSuchElementException:
        print('❌ Best Deals offer heading is not available')

    # verify the quantity of offer item(s) inside the offer card and above the img
    try:
        offer_qty = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_quantity'))
        )
        print(f'✅ Offer Qty: {offer_qty.text} is available')
    except NoSuchElementException:
            print('⚠️ Offer Qty is not only 1 qty is the max_redeem for the offer item available')
    # verify the price of offer item(s) above the img inside the offer card
    try:
        offer_price = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_price'))
        )
        print(f'✅ Offer Price : {offer_price.text} is available')
    except NoSuchElementException:
        print('❌ Offer Price is not available')

    # verify the multi sku deals cards
    try:
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/sku_deals_cardview'))
        )
        print('✅ Best Deals Card View is available')
    except NoSuchElementException:
        print('❌ Best Deals Card View is NOT available')

    # verify the offer image is available on the card
    try:
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/offer_image_view'))
        )
        print('✅ Offer Image inside the card is available')
    except NoSuchElementException:
        print('❌  Offer Image inside the card is NOT available')



    # verify the title of the offer inside the offer card
    try:
        offer_heading_inside_card = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_product_name'))
        )
        print(f'✅ {offer_heading_inside_card.text} Card Title is available')
    except NoSuchElementException:
        print('❌  Card Title is NOT available')

    # verify the subtitle and the offer state buttons, MOVs, and the progress bar of the offer inside the offer card
    try:
        # verify the body text to confirm whether the offer is locked or unlocked
        offer_subtitle_inside_card = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_product_details'))
        )

        # when the offer is unlocked
        if offer_subtitle_inside_card.text == "Yay! Special Deal Unlocked":

            print(f'✅ Offer is UNLOCKED, and Offer Subtitle: {offer_subtitle_inside_card.text}, inside card is available')

            # verify unlocked button is available
            try:
                choose_item_btn = wait.until(
                    EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_choose_items'))
                )
                print(f'✅ {choose_item_btn.text} button is available')
            except NoSuchElementException:
                print('❌ Choose an item button is NOT available')

        # when the offer is locked
        else:
            print(f'✅  Offer is LOCKED / OOS, and Offer Subtitle: {offer_subtitle_inside_card.text}, text inside card is available')
            print('Checking whether the offer is LOCKED or OOS...')
            try:
                locked_card_verification(wait)
            except NoSuchElementException:
                print('No Locked Deals found!')


    except NoSuchElementException:
        print('❌ Offer Body text inside card is NOT available')


def locked_card_verification(wait):

    # getting the button text so that we can distinguish whether the locked offer is locked or OOS
    button_element = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btn_add_products"))
    )

    #verify the correspondence elements if the offer is locked
    if button_element.text.lower() == "locked":
        print('Offer is LOCKED!')
        print('Verifying the elements of locked state of an offer...')
        # verify the MOV text
        try:
            mov_text = wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_subtitle'))
            )
            print(f'✅ MOV text : {mov_text.text}, is available')
        except NoSuchElementException:
            print('❌ MOV text is NOT available')

        # verify the progress bar
        try:
            progress_prcnt = wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/progress_offer'))
            )
            print(f'✅ Progress Bar with {progress_prcnt.text}% is available')
        except NoSuchElementException:
            print('❌ Progress Bar is NOT available')

        # verify unlocked disables button
        try:
            # 3. Check both conditions
            if not button_element.is_enabled():
                print(f"✅ Button is correctly disabled.")
            else:
                if button_element.is_enabled():
                    print(f"❌ Button is enabled, but should be disabled.")

                print("locked disable button is not available")

        except TimeoutException:
            print(f"❌ Button element with ID 'btn_add_products' not found.")
            print("locked disable button is not available")

    else:
        print('Offer is OOS')
        print('Verifying the elements of OOS state of an offer...')

        # check whether sold is written over the button or not
        if button_element.text.lower() == "sold":
            print(f'Button with: {button_element.text} is available')

        #verify the SOLD OUT watermarks over the product img
        try:
            sold_out_watermark = wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/iv_sold_out'))
            )
            print('SOLD OUT Watermark is available')
        except NoSuchElementException:
            print('SOLD OUT Watermark is NOT available')

        # verify the MOV text
        try:
            offer_state_msg = wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_subtitle'))
            )
            print(f'✅ Offer State Message: {offer_state_msg.text}, is available')
        except NoSuchElementException:
            print('❌ Offer State Message text is NOT available')

        # verify the progress bar
        try:
            progress_prcnt = wait.until(
                EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/progress_offer'))
            )
            print(f'✅ Progress Bar with {progress_prcnt.text}% is available')
        except NoSuchElementException:
            print('❌ Progress Bar is NOT available')

        # verify unlocked disables button
        try:
            # 3. Check both conditions
            if not button_element.is_enabled():
                print(f"✅ Button is correctly disabled.")
            else:
                if button_element.is_enabled():
                    print(f"❌ Button is enabled, but should be disabled.")

                print("SOLD disable button is not available")

        except TimeoutException:
            print(f"❌ Button element with ID 'btn_add_products' not found.")
            print("locked disable button is not available")