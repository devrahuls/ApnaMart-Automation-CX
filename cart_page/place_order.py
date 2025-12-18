import time

from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def place_order_cod(driver, wait, address):

    '''
        prerequisite:
            At least one item should be Added To Cart, open the cart page.
            The selected address store should be Online.
    '''

    try:
        add_delivery_address = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add Delivery Address")'))
        )
        add_delivery_address.click()

        confirm_address_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                        'new UiSelector().text("Confirm Location")'))
        )
        confirm_address_btn.click()

        change_address_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/changeButton"))
        )
        change_address_btn.click()

        address_search_bar = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
        )
        address_search_bar.click()

        set_address_search = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
        )
        set_address_search.send_keys(address)

        first_search_result = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tvCategory"))
        )
        first_search_result.click()

        confirm_address_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                        'new UiSelector().text("Confirm Location")'))
        )
        confirm_address_btn.click()

        house_name = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID,'com.apnamart.apnaconsumer:id/et_cvv'))
        )
        house_name.click()
        house_name.send_keys("test00")

        save_add_as_others = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID,'com.apnamart.apnaconsumer:id/tvCategory'))
        )
        save_add_as_others.click()

        save_add_as_others_name = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID,'com.apnamart.apnaconsumer:id/etSaveAddressAs'))
        )
        save_add_as_others_name.click()
        save_add_as_others_name.send_keys("TEST00")

        save_and_continue = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                        'new UiSelector().text("Save and Continue")'))
        )
        save_and_continue.click()

    except:
        pass

    time.sleep(5)

    # Payment selection
    payment_mode_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select Payment Mode")'))
    )
    payment_mode_btn.click()

    cod_option = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cash On Delivery")'))
    )
    cod_option.click()

    confirm_btn = wait.until(EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.Button")))
    confirm_btn.click()

    place_order_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR,
                                                             'new UiSelector().text("Place Order")')))
    place_order_btn.click()

    print("Order is placing via COD")
    print("✅ View Cart & Place Order Flow Completed.")