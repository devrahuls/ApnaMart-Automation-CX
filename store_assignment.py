from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from update_app_request_bottomsheet import remove_update_app_bottomsheet

#1.  com.apnamart.apnaconsumer:id/allow_access_button
# 2. com.apnamart.apnaconsumer:id/select_address_button
# 1. com.apnamart.apnaconsumer:id/grantButton
# new UiSelector().text("Permissions")
# new UiSelector().text("Location")
# new UiSelector().text("Allow only while using the app")
# new UiSelector().description("Navigate up")
# new UiSelector().description("Navigate up")
# new UiSelector().className("android.widget.Button").instance(3)
# click on the middle of the screen - a bit up from the middle of the screen

def store_assignment(driver, wait, address):
    try:
        service_unavailable_text_confirmation = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_delivering_in"))
        )
        if service_unavailable_text_confirmation.text == "Service Unavailable!":
            click_on_the_tv = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/tv_delivering_in"))
            )
            click_on_the_tv.click()

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

        # remove the update request bottomsheet
        remove_update_app_bottomsheet(wait)



    except:
        print("Current location store is available")