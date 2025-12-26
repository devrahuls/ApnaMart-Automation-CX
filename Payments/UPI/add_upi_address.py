import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from global_variables import *

def add_upi_address(driver, wait, UPI_ADDRESS):
    add_upi_address = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add your UPI address")'))
    )
    add_upi_address.click()

    enter_upi_address = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter UPI ID")'))
    )
    enter_upi_address.clear()
    enter_upi_address.send_keys(UPI_ADDRESS)

    verify_and_select_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.XPATH, 'new UiSelector().className("android.widget.Button")'))
    )
    verify_and_select_btn.click()



def edit_upi_address(driver, wait):
    edit_upi_add_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(7)'))
    )
    edit_upi_add_btn.click()

    delete_specific_upi_id(driver, wait, WRONG_UPI)






def delete_specific_upi_id(driver, wait, target_upi):
    print(f"\n--- Searching for UPI ID: {target_upi} ---")

    try:
        # 1. Store all UPI ID titles into an array
        # We wait for the list to be present
        upi_title_elements = wait.until(EC.presence_of_all_elements_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.apnamart.apnaconsumer:id/payment_title"]')
        ))

        upi_ids_list = [el.text.strip() for el in upi_title_elements]
        print(f"Found UPI IDs: {upi_ids_list}")

        # 2. Find the index of the specific ID
        target_index = -1
        for index, upi_id in enumerate(upi_ids_list):
            if upi_id == target_upi:
                target_index = index
                break

        if target_index != -1:
            print(f"✅ Match found at index {target_index} (Position {target_index + 1})")

            # 3. Locate the delete button corresponding to that index
            # We use the instance() method in UIAutomator to click the specific button
            delete_btn_selector = f'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/img_check").instance({target_index})'

            delete_button = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, delete_btn_selector)

            # 4. Click the delete button
            delete_button.click()
            print(f"🗑️ Clicked delete button for {target_upi}")

            # Optional: Wait for UI to update or handle a "Confirm Delete" popup
            time.sleep(1)

        else:
            print(f"❌ Target UPI ID '{target_upi}' not found in the list.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
