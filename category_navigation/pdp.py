from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from driver_setup import get_driver, get_wait
from category_navigation.plp import vertical_scroll_till_end


def pdp(wait):

    print("--- Starting PDP Test Cases ---")

    first_product_on_HP = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/ivProduct").instance(0)')))
    first_product_on_HP.click()

    #Check whether the product img is available
    try:
        is_product_image = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/ivProductFilled')))
        is_product_image.click()

        print("✅ Product Image is available")

        close_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(1)')))
        close_btn.click()
    except:
        print("❌ No product image available")

    #Check whether the product highlighted texts is available
    try:
        is_product_highlighted_text = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/highlightText')))
        is_product_highlighted_text.click()
        print("✅ Product highlighted text is available")
    except:
        print("❌ No product highlighted text available")

    #Check whether the product name is available
    try:
        is_product_name = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/item_name')))

        print(f"✅ Product name is available : {is_product_name.text}")
    except:
        print("❌ No product name available")

    #Check whether the product unit is available
    try:
        is_product_unit = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/productUnitBottom')))

        print(f"✅ Product unit is available : {is_product_unit.text}")
    except:
        print("❌ No product unit available")

    try:
        is_product_selling_price = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tvProductSellingPriceBottom')))

        sp_with_rupee_symbol = is_product_selling_price.text
        sp_value = int(sp_with_rupee_symbol.replace("₹", ""))


        if sp_value > 0:
            print(f"✅ Product selling price is available : {is_product_selling_price.text}")
        else:
            print(f"⚠️ Selling price is in negative : {is_product_selling_price.text}")
    except:
        print("❌ No product selling price available")


    try:
        is_product_mrp = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tvProductMarketPriceBottom')))

        mrp_with_rupee_symbol = is_product_mrp.text
        mrp_value = int(mrp_with_rupee_symbol.replace("₹", ""))

        if mrp_value > 0 and mrp_value > sp_value:
            print(f"✅ Product MRP is available at : {is_product_mrp.text}, which is less than SP {is_product_selling_price.text}.")
        else:
            print(f"⚠️ MRP is in negative OR less than SP : {is_product_mrp.text}")
    except:
        print("❌ No Product MRP available")

    try:
        is_price_off_on_mrp = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/textView')))

        print(f"✅ Ruppee/Percentage off on MRP is available : {is_price_off_on_mrp.text}")

    except:
        print("❌ No Price off on MRP available")



def product_attributes(driver, wait):
    print("--- Starting Verifying Product Attributes on PDP---")

    first_product_on_HP = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/ivProduct").instance(0)')))
    first_product_on_HP.click()

    # VERIFY PRODUCT HIGHLIGHTS
    print("--- Starting Verifying Product Highlights ---")
    try:
        verify_product_highlights = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Product Highlights")')))
        print(f'✅ {verify_product_highlights.text} is available')
    except:
        print('❌ Product highlights is not available')

    # Scroll till the end so that all product highlight keys gets visible on the viewport
    vertical_scroll_till_end(driver, 2)

    # verify product highlights keys
    try:
        product_highlight_key00 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Product Type")')))
        print(f'✅ {product_highlight_key00.text} key is available')
    except:
        print('❌ Product Type key is not available')

    try:
        product_highlight_key01 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Brand")')))
        print(f'✅ {product_highlight_key01.text} key is available')
    except:
        print('❌ Brand key is not available')

    try:
        product_highlight_key02 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Item Form")')))
        print(f'✅ {product_highlight_key02.text} key is available')
    except:
        print('❌ Item Form key is not available')

    # Closing the Product Highlight toggler so that all Product Attributes comes into the viewport
    verify_product_highlights.click()


    # VERIFY PRODUCT SPECIFICATIONS
    try:
        verify_specifications = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Specifications")')))
        print(f'✅ {verify_specifications.text} is available')

    except:
        print('❌ Specifications is not available')

    verify_specifications.click() #Open the specification toggler so that all keys gets visible on the screen

    # since specifications has so many keys and cant be listed in a single viewport,
    # we vertically scroll only a bit so that none of the keys gets left behind from the viewport and verification
    vertical_scroll_till_end(driver, 1)

    # Verifying the product specifications keys
    try:
        product_specification_key00 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Manufacturer")')))
        print(f'✅ {product_specification_key00.text} key is available')
    except:
        print('❌ Manufacturer key is not available')

    try:
        product_specification_key01 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Country of Origin")')))
        print(f'✅ {product_specification_key01.text} key is available')
    except:
        print('❌ Country of Origin key is not available')

    try:
        product_specification_key02 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Key Features")')))
        print(f'✅ {product_specification_key02.text} key is available')
    except:
        print('❌ Key Features key is not available')

    try:
        product_specification_key03 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("FSSAI License")')))
        print(f'✅ {product_specification_key03.text} key is available')
    except:
        print('❌ FSSAI License key is not available')

    try:
        product_specification_key04 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Customer Care Details")')))
        print(f'✅ {product_specification_key04.text} key is available')
    except:
        print('❌ Customer Care Details key is not available')

    try:
        product_specification_key05 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("asfhbnsdi")')))
        print(f'✅ {product_specification_key05.text} key is available')
    except:
        print('❌ BOOMBAMM key is not available')

    # Scrolling till the end so that all of the rest keys gets onto the viewport
    vertical_scroll_till_end(driver, 1)

    try:
        product_specification_key06 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Disclaimer")')))
        print(f'✅ {product_specification_key06.text} key is available')
    except:
        print('❌ Disclaimer key is not available')

    try:
        verify_return_refund_policy = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Return and Refund Policy")')))
        print(f'✅ {verify_return_refund_policy.text} is available')

    except:
        print('❌ Return and Refund Policy is not available')

    # click on the toggle so that we can see the keys of it
    verify_return_refund_policy.click()

    # scroll till end so that we can see all of the keys of return and refund policy attributes
    vertical_scroll_till_end(driver, 1)

    # Verify the Return and Refund Policy keys
    try:
        return_refund_policy_key00 = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Return Policy")')))
        print(f'✅ {return_refund_policy_key00.text} key is available')

    except:
        print('❌ Return Policy key is not available')


def share_product(driver, wait):

    first_product_on_HP = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/ivProduct").instance(0)')))
    first_product_on_HP.click()

    print("--- Starting Verifying the Product Share---")
    try:
        product_share_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(3)')))
        product_share_btn.click()

        sharing_link_bottomsheet = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.android.intentresolver:id/headline')))
        print(f'{sharing_link_bottomsheet.text} is available')
    except:
        print('❌ Share Product Button is not available')