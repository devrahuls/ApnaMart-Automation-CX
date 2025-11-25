from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

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


def wholesale_verification(wait):

    verify_vip_offer_wholesale_bottomsheet(wait) #verify vip-offer wholesale-bottomsheet

    first_product_tile = wait.until(
        EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/ivProduct").instance(0)'))
    )
    first_product_tile.click()
    print('clicked on the first product tile.')

    verify_vip_offer_wholesale_bottomsheet(wait) #verify vip-offer wholesale-bottomsheet

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

    try:
        wholesale_cart_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.view.View[@resource-id="Wholesale Cart"]'))
        )
        wholesale_cart_btn.click()
        print("✅ Redirected to the Wholesale Cart.")
    except TimeoutException:
        print("❌ Unable to Redirect to the Wholesale Cart.")

    try:
        wholesale_cart_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.view.View[@resource-id="Wholesale Cart"]'))
        )
        wholesale_cart_btn.click()
        print("✅ Redirected to the Wholesale Cart.")
    except TimeoutException:
        print("❌ Unable to Redirect to the Wholesale Cart.")



