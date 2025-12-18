import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def verify_empty_cart(wait):

    wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/loader'))
    )
    print(f'✅ Empty Cart Box Animation is available!')

    cart_empty_title = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/noItemsText'))
    )
    print(f'✅ Title text : {cart_empty_title.text} , is available!')

    cart_empty_subtitle = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/emptyTextTwo'))
    )
    print(f'✅ Subtitle text : {cart_empty_subtitle.text} , is available!')

    start_shopping_home_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/homeButton'))
    )
    start_shopping_home_btn.click()

    print('✅ Empty cart is working fine, successfully redirected to home page after clicking start shopping btn.')

def empty_cart_flow(driver, wait):
    print("\n--- Starting Empty Cart Flow ---")

    # Define the locators
    minus_btn_selector = 'new UiSelector().resourceId("product quantity negative").instance(0)'
    empty_cart_id = "com.apnamart.apnaconsumer:id/emptyView"

    try:
        while True:
            # 1. Check if the emptyView is visible
            # We use a short timeout (1-2 seconds) so the loop doesn't hang
            try:
                empty_view = driver.find_elements(AppiumBy.ID, empty_cart_id)
                if len(empty_view) > 0 and empty_view[0].is_displayed():
                    print("✅ Cart is empty. 'emptyView' detected.")
                    break
            except Exception:
                pass  # Keep going if not found yet

            # 2. Try to find and click the minus button of the first item
            try:
                # We use a short wait to see if the button is still there
                minus_btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, minus_btn_selector)
                minus_btn.click()
                print("Clicked '-' on the first item...")

                # Small sleep to allow the app to process the deletion/UI shift
                time.sleep(0.8)
            except NoSuchElementException:
                # If minus button is gone but emptyView hasn't appeared,
                # maybe the app is still loading
                print("Waiting for UI to refresh...")
                time.sleep(2)

                # Final check for empty view before giving up
                if len(driver.find_elements(AppiumBy.ID, empty_cart_id)) > 0:
                    print("✅ Cart is now empty.")
                    break
                else:
                    print("🛑 No minus button and no empty view. Stopping loop.")
                    break

    except Exception as e:
        print(f"❌ An error occurred while emptying the cart: {e}")

    verify_empty_cart(wait)
