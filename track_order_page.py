from global_variables import *
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from scroll_until_find_an_element import scroll_down_to_find_an_element, scroll_till_end_of_page
import re
from selenium.common.exceptions import TimeoutException, NoSuchElementException





def gather_ordered_product_details(driver, wait):
    # Initialize arrays
    product_images = []
    product_names = []
    product_prices = []
    product_units_qty = []

    try:
        # Wait for the product names to be visible to ensure the list has loaded
        wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/productName")))

        # 1. Gather Image sources (usually 'content-desc' or 'text' is empty for images,
        # so we check if you need the resource ID or a specific attribute)
        images = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/ivProduct")
        for img in images:
            # For images, we usually store the content-description or verify existence
            product_images.append(img.get_attribute("content-desc") or "image_present")

        # 2. Gather Product Names
        names = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/productName")
        product_names = [name.text for name in names]

        # 3. Gather Product Prices
        prices = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/tvProductMarketPrice")
        product_prices = [price.text for price in prices]

        # 4. Gather Units and Quantity
        units = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/tvProductQuantity")
        product_units_qty = [unit.text for unit in units]

        if len(product_images) == len(product_names) == len(product_prices) == len(product_units_qty):
            print(f"✅ Successfully gathered {len(product_names)} items from the cart.")
        else:
            print("❌ Data Mismatch between either of product images or product names or prices or product units.")

        # Return as a dictionary of arrays for easy access
        return {
            "images": product_images,
            "names": product_names,
            "prices": product_prices,
            "units_qty": product_units_qty
        }

    except Exception as e:
        print(f"❌ Failed to gather product elements: {e}")
        return None




def validate_savings(driver, wait, bill_names, bill_amounts, strikethrough_prices):
    """
    Validates savings by:
    1. Calculating (Strikethrough - Bill Amount) for each item, skipping 'Offer Savings'.
    2. Adding the 'Offer Savings' amount itself to that total.
    3. Comparing against the Banner Saving Text.
    """
    try:
        print("\n--- Savings Validation (Updated Logic) ---")

        # 1. Get the Banner Saving Text (e.g., 'Saving ₹219 on this order.')
        saving_element = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/saving_text"))
        )
        banner_text = saving_element.text
        extracted_numbers = re.findall(r'\d+', banner_text.replace(',', ''))
        banner_saving_amt = float(extracted_numbers[0]) if extracted_numbers else 0.0

        # 2. Initialize variables for calculation
        item_savings_total = 0.0
        offer_savings_amt = 0.0

        # 3. Iterate through bill items to calculate (Strikethrough - Price)
        # Note: We use the length of strikethrough_prices as the limit for item comparison
        for i in range(len(strikethrough_prices)):
            # Check if this index in bill_names is 'Offer Savings'
            if i < len(bill_names) and bill_names[i] == "Offer Savings":
                print(f"Index {i}: Found 'Offer Savings', skipping subtraction.")
                continue

            # Clean Strikethrough Price (e.g., '₹50')
            strike_val = float(strikethrough_prices[i].replace('₹', '').replace(',', '').strip())

            # Get corresponding Bill Amount (Selling Price)
            bill_val = bill_amounts[i]

            # Calculate difference: Individual Item Saving = MRP - Selling Price
            diff = strike_val - bill_val
            item_savings_total += diff
            print(f"Item {i}: {strike_val} (MRP) - {bill_val} (Price) = {diff} saved")

        # 4. Handle the 'Offer Savings' (Coupon) separately
        # If 'Offer Savings' exists in bill_amounts, we add its absolute value to total savings
        if "Offer Savings" in bill_names:
            offer_index = bill_names.index("Offer Savings")
            offer_savings_amt = abs(bill_amounts[offer_index])
            print(f"🎟️ Adding Offer Savings (Coupon): {offer_savings_amt}")

        # 5. Final Calculation
        calculated_total_savings = item_savings_total + offer_savings_amt
        print(
            f"🧮 Total Calculated: {item_savings_total} (Item Diff) + {offer_savings_amt} (Offer) = {calculated_total_savings}")

        # Final Match check
        if round(calculated_total_savings, 2) == round(banner_saving_amt, 2):
            print(f"✅ Savings Match! Calculated ({calculated_total_savings}) equals Banner ({banner_saving_amt})")
        else:
            print(f"❌ Savings Mismatch! Calculated: {calculated_total_savings}, Banner: {banner_saving_amt}")

    except Exception as e:
        print(f"❌ Error during savings validation: {e}")



def validate_bill_details(driver, wait):
    bill_names = []
    bill_amounts = []
    strikethrough_prices = []

    try:
        # 1. Gather text_sub_total (Names)
        name_elements = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/text_sub_total")
        bill_names = [el.text for el in name_elements]

        # 2. Gather amount_sub_total (Prices) and Clean them
        amount_elements = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/amount_sub_total")
        for el in amount_elements:
            # Remove ₹ but keep the '-' sign if present
            clean_val = el.text.replace('₹', '').strip()
            bill_amounts.append(float(clean_val))

        # 3. Gather total_selling_price (Optional Strikethrough)
        strike_elements = driver.find_elements(AppiumBy.ID, "com.apnamart.apnaconsumer:id/total_selling_price")
        strikethrough_prices = [el.text for el in strike_elements]

        # --- DATA PRINTOUT ---
        print("\n--- Bill Details ---")
        for name, amt in zip(bill_names, bill_amounts):
            print(f"{name}: {amt}")

        # --- OFFER SAVINGS CHECK ---
        if "Offer Savings" in bill_names:
            try:
                offer_applied = driver.find_element(AppiumBy.ID, "com.apnamart.apnaconsumer:id/text_offer_applied")
                print(f"✅ Coupon Found: {offer_applied.text}")
            except NoSuchElementException:
                print("❌ Offer Savings exists, but coupon code could not be found.")

        # --- MATHEMATICAL VALIDATION ---
        if bill_names[-1] == "To Pay":
            actual_to_pay = bill_amounts[-1]
            calculated_sum = sum(bill_amounts[:-1])  # Sum everything except the last index

            print(f"\nCalculated Sum: {calculated_sum}")
            print(f"Displayed 'To Pay': {actual_to_pay}")

            if round(calculated_sum, 2) == round(actual_to_pay, 2):
                print("✅ Bill Validation Successful: Calculations match the 'To Pay' amount.")
            else:
                print(f"❌ Bill Validation Failed: Expected {calculated_sum}, but found {actual_to_pay}")
        else:
            print("⚠️ The last item in the list is not 'To Pay'. Skipping math validation.")

    except Exception as e:
        print(f"❌ Error during bill gathering: {e}")

    validate_savings(driver, wait, bill_names, bill_amounts, strikethrough_prices)







def ongoing_track_order_page_verification(driver, wait):

    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/topAppBar'))
    )
    print(f'Track Order Page Heading is Displaying')

    back_btn = wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Navigate up")'))
    )
    print(f'Track Order Page Back Btn is Displaying')

    track_order_page_header_title = wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Track Order")'))
    )
    print(f'Track Order Page Header Title : {track_order_page_header_title.text} is Displaying')

    tracking_view_box = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tracking_view'))
    )
    print(f'Tracking View Box is Displaying')

    delivery_time_layout = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/layout_delivery_time'))
    )
    print(f'Delivery Time Layout is Displaying')

    delivery_time_layout_title = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/deliveryTimeText'))
    )
    print(f'Delivery Time Title : {delivery_time_layout_title.text} is Displaying')

    delivery_time_layout_time = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/delivery_time'))
    )
    print(f'Delivery Time : {delivery_time_layout_time.text} is Displaying')

    delivery_animation = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/animationView'))
    )
    print(f'Delivery Animation is Displaying')

    delivery_status_layout = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/status_layout'))
    )
    print(f'Delivery Status Layout is Displaying')

    delivery_packing_status = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/packingText'))
    )
    print(f'Delivery {delivery_packing_status.text} Status is Displaying')

    delivery_ontheway_status = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/onTheWayText'))
    )
    print(f'Delivery {delivery_ontheway_status.text} Status is Displaying')

    delivery_arrived_status = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/arrived'))
    )
    print(f'Delivery {delivery_arrived_status.text} Status is Displaying')

    pay_online_now_layout = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/payment_process'))
    )
    print(f'Pay Online Now Layout is Displaying')

    pay_online_now_icon = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/payment_icon'))
    )
    print(f'Pay Online Now Icon is Displaying')

    pay_online_now_heading = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/payment_icon'))
    )
    print(f'Pay Online Now Heading: {pay_online_now_heading.text} is Displaying')

    pay_online_now_subheading = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/pay_now_sub_heading'))
    )
    print(f'Pay Online Now Sub-Heading: {pay_online_now_subheading.text} is Displaying')

    pay_online_now_btn = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_pay_now'))
    )
    print(f'Pay Online Now Btn: {pay_online_now_btn.text} is Displaying')

    order_info_card = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/order_info_card_1'))
    )
    print(f'Order Info Card is Displaying')

    delivery_location_layout = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/del_loc_layout'))
    )
    print(f'Delivery Location Layout inside Order Info Card is Displaying')

    delivery_location_layout_img = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/del_loc_Img'))
    )
    print(f'Delivery Location Layout Image is Displaying')

    delivery_location_text = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/del_loc_TextTitle'))
    )
    print(f'Delivery Location Text is Displaying')

    delivery_location_store_name = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/del_loc_TextSubTitle'))
    )
    print(f'Delivery Location Store Name is Displaying')

    order_id_layout = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/order_id_layout'))
    )
    print(f'Order-ID Layout is Displaying')

    order_id_number = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/order_id_TextTitle'))
    )
    print(f'Order-ID Number :{order_id_number.text}, is Displaying')

    ordered_time = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/order_id_TextSubTitle'))
    )
    print(f'Ordered Time :{ordered_time.text} is Displaying')


    #CHAT WITH US COMPONENT
    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/chat_with_us_layout'))
    )
    print(f'CHAT WITH US / HELP LAYOUT is Displaying')

    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/chat_with_us_img'))
    )
    print(f'CHAT WITH US Image is Displaying')

    chat_with_us_title = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/chat_with_us_TextTitle'))
    )
    print(f'CHAT WITH US Title: {chat_with_us_title.text} is Displaying')

    chat_with_us_subtitle = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/chat_with_us_TextSubTitle'))
    )
    print(f'CHAT WITH US Subtitle: {chat_with_us_subtitle.text} is Displaying')

    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/chat_icon_forward'))
    )
    print(f'CHAT WITH US Forward Icon to Open is Displaying')


    # order list verification
    '''
    gather count
    gather name, check no duplicates in array on every loop
    if no duplicate gather other details related to the ordered item     
    else skip
    '''
    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/orderItemCard'))
    )
    print(f'Ordered Item Card is Displaying')

    ordered_items_count = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/itemListText'))
    )
    print(f'Order Item Count : {ordered_items_count.text} is Displaying')

    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/orderItemCard'))
    )
    print(f'Ordered Item Card is Displaying')

    # so that all item list get display
    scroll_down_to_find_an_element(driver, AppiumBy.ID, 'com.apnamart.apnaconsumer:id/container_order_summary', 5)


    # 1. Call the function
    cart_data = gather_ordered_product_details(driver, wait)

    # 2. Check if data was successfully gathered
    if cart_data:
        print("\n--- Gathered Cart Details ---")

        # Get the number of products found (based on the name array)
        num_products = len(cart_data['names'])

        for i in range(num_products):
            print(f"Product {i + 1}:")
            print(f"  - Name: {cart_data['names'][i]}")
            print(f"  - Price: {cart_data['prices'][i]}")
            print(f"  - Unit/Qty: {cart_data['units_qty'][i]}")
            print(f"  - Image Info: {cart_data['images'][i]}")
            print("-" * 30)
    else:
        print("No data was gathered from the cart.")



    ordered_number = int(re.search(r'\d+', ordered_items_count.text).group())

    if ordered_number == len(cart_data['names']):
        print("✅ All Items Has Been Successfully Gathered and Verified.")


    # Bill Verification
    scroll_till_end_of_page(driver, 10)

    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/container_order_summary_card'))
    )
    print(f'Order Bill Card is Displaying')

    bill_heading = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/text_heading'))
    )
    print(f'Order Bill Heading: {bill_heading.text} is Displaying')

    validate_bill_details(driver, wait)





