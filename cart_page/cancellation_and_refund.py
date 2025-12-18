from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scroll_until_find_an_element import scroll_down_to_find_an_element

def cancellation_and_refund_policy(driver, wait):
    print("\nOpening Cancellation & Refund Policy Bottomsheet...")

    try:
        cancellation_and_refund_bottomsheet = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cancellation & Refund Policy")')))
        cancellation_and_refund_bottomsheet.click()
        print("✅ Cancellation & Refund Policy has Found.")
    except NoSuchElementException as e:
        print(f"❌ Cancellation & Refund Policy could not be found\nReason: {e}.")

    try:
        cnr_header_title = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/header_title')))
        print(f"✅ Header Title has found : {cnr_header_title.text}")
    except NoSuchElementException as e:
        print("❌ Header of the Bottomsheet could not be found!")

    try:
        wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/order_cancellation_image')))
        wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/line_view')))
        print(f"✅ Cancel Image with Line View has found!")
    except NoSuchElementException as e:
        print("❌ Cancel Image with Line View could not be found!")

    try:
        order_cancellation_text = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/order_cancellation_text')))
        print(f"✅ Order Cancellation Text has found : {order_cancellation_text.text}")
    except NoSuchElementException as e:
        print("❌ Order Cancellation Text could not be found!")

    try:
        order_cancellation_text = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/order_cancellation_text')))
        print(f"✅ Order Cancellation Text has found : {order_cancellation_text.text}")
    except NoSuchElementException as e:
        print("❌ Order Cancellation Text could not be found!")

    try:
        cnr_conditions = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH,
            '//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/order_cancellation_condition_one"]')))
        print(f"✅ Order Cancellation and Refund Conditions Text has found : {cnr_conditions.text}")
    except NoSuchElementException as e:
        print("❌ Order Cancellation and Refund Conditions Text could not be found!")


    try:
        print('Closing the Bottomsheet...')
        close_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/close_btn')))
        close_btn.click()
        print("✅ Bottomsheet Closed Successfully!")
    except NoSuchElementException as e:
        print("❌ Click Button could not be found!")

    print('🎉 All Elements of the Terms And Condition Bottomsheet has been verified')


