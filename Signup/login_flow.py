from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver
from time import sleep
from update_app_request_bottomsheet import remove_update_app_bottomsheet

from selenium.webdriver.support.wait import WebDriverWait
import time


def login_flow(driver, wait):
    try:
        # Location permission
        location_grant_access = wait.until(
            EC.presence_of_element_located((AppiumBy.ID,
                "com.android.permissioncontroller:id/permission_allow_foreground_only_button"))
        )
        location_grant_access.click()

        # Language selection
        language_selection_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID,
                "com.apnamart.apnaconsumer:id/language_selection_button"))
        )
        language_selection_button.click()

        # remove the update request bottomsheet
        remove_update_app_bottomsheet(driver)

        # Truecaller flow
        try:
            truecallerConfirmBtn = wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "com.truecaller:id/tv_confirm"))
            )
            print("Truecaller detected, logging in...")
            truecallerConfirmBtn.click()
        except TimeoutException:
            print("Truecaller not found, logging in via phone number...")

            # Step 1: Find and click the phone input field to trigger any popups
            phone_input = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/phoneInputEditText"))
            )
            phone_input.click()

            # Step 2: Handle the "None of the above" autofill suggestion popup, if it appears
            try:
                none_of_above = wait.until(
                    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("NONE OF THE ABOVE")'))
                )
                none_of_above.click()
                print("Dismissed the 'None of the above' popup.")
            except TimeoutException:
                print("No 'None of the above' popup appeared.")

            # Step 3: Re-locate the input field, CLICK to restore focus, then send keys
            # This is the crucial part. We find it again to get a fresh reference.
            phone_input_to_fill = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/phoneInputEditText"))
            )
            # **CLICK AGAIN** to ensure the element has focus and the keyboard is active.
            phone_input_to_fill.click()

            # sleep(0.5)

            phone_input_to_fill.send_keys("9999999999")

            continue_btn = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/continueWithPhone"))
            )
            continue_btn.click()

            otp_input = wait.until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )
            otp_input.send_keys("432967")

        time.sleep(1)

        # Notifications
        notification_permission_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"))
        )
        notification_permission_btn.click()

        remove_update_app_bottomsheet(driver)

        print("✅ Login flow completed.")

    except Exception as e:
        print(f"❌ Login flow failed: {e}")
        raise e



def custom_login(driver, wait):
    try:
        # Location permission
        location_grant_access = wait.until(
            EC.presence_of_element_located((AppiumBy.ID,
                                            "com.android.permissioncontroller:id/permission_allow_foreground_only_button"))
        )
        location_grant_access.click()

        # Language selection
        language_selection_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID,
                                        "com.apnamart.apnaconsumer:id/language_selection_button"))
        )
        language_selection_button.click()

        # Truecaller flow
        try:
            truecallerConfirmBtn = wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "com.truecaller:id/tv_confirm"))
            )
            print("Truecaller detected, logging in...")
            truecallerConfirmBtn.click()
        except TimeoutException:
            print("Truecaller not found, logging in via phone number...")

            # Step 1: Find and click the phone input field to trigger any popups
            phone_input = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/phoneInputEditText"))
            )
            phone_input.click()

            # Step 2: Handle the "None of the above" autofill suggestion popup, if it appears
            try:
                none_of_above = wait.until(
                    EC.element_to_be_clickable(
                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("NONE OF THE ABOVE")'))
                )
                none_of_above.click()
                print("Dismissed the 'None of the above' popup.")
            except TimeoutException:
                print("No 'None of the above' popup appeared.")

            # Step 3: Re-locate the input field, CLICK to restore focus, then send keys
            # This is the crucial part. We find it again to get a fresh reference.
            phone_input_to_fill = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/phoneInputEditText"))
            )
            # **CLICK AGAIN** to ensure the element has focus and the keyboard is active.
            phone_input_to_fill.click()

            # sleep(0.5)

            phn_no = int(input("Enter phone number: "))
            phone_input_to_fill.send_keys(phn_no)

            continue_btn = wait.until(
                EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/continueWithPhone"))
            )
            continue_btn.click()

            # Create a special wait with a longer timeout just for the resend button
            long_wait = WebDriverWait(driver, 40)
            otp_entered_successfully = False

            # Loop until the user confirms the OTP has been entered
            while not otp_entered_successfully:
                print("\nDid you receive the OTP?")
                # Use try-except to handle non-integer inputs gracefully
                try:
                    is_otp_receive = int(input("Enter 1 for Yes or 0 for No: "))
                except ValueError:
                    print("Invalid input. Please enter 1 or 0.")
                    continue  # Ask the question again

                if is_otp_receive == 1:
                    otp = input("Enter the OTP code: ")
                    otp_input = wait.until(
                        EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
                    )
                    otp_input.send_keys(otp)

                    # Set the flag to True to exit the while loop
                    otp_entered_successfully = True
                    print("✅ OTP Entered. Continuing...")

                elif is_otp_receive == 0:
                    print("Waiting for the resend button to become active (up to 30 seconds)...")
                    # try:
                    #     # Use the long_wait to wait until the button is clickable
                    #     resend_otp_btn = long_wait.until(
                    #         EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/resendOtp"))
                    #     )
                    #     resend_otp_btn.click()
                    #     print("✅ Resend OTP button clicked. Please check for the new OTP.")
                    # except Exception as e:
                    #     print(f"❌ Could not click the resend OTP button. Error: {e}")
                    #     # Break the loop if the button is never found to avoid an infinite loop
                    #     break

                    # --- Custom Keep-Alive Loop ---
                    resend_button_clicked = False
                    # start_time = time.time()
                    # Loop for a maximum of 40 seconds
                    while 30 < 40:
                        try:
                            # Quickly check if the button is present and enabled
                            resend_otp_btn = driver.find_element(AppiumBy.ID, "com.apnamart.apnaconsumer:id/resendOtp")
                            if resend_otp_btn.is_enabled():
                                resend_otp_btn.click()
                                print("✅ Resend OTP button clicked. Please check for the new OTP.")
                                resend_button_clicked = True
                                break  # Exit the inner while loop
                        except NoSuchElementException:
                            # The button isn't even in the layout yet, so we wait.
                            pass

                        # Wait for 5 seconds before the next check. This keeps the session active.
                        print("Button not active yet. Checking again in 5 seconds...")
                        time.sleep(5)

                    if not resend_button_clicked:
                        print("❌ Resend OTP button did not become active within 40 seconds.")
                        break  # Exit the main while loop to prevent getting stuck
        else:
            print("Invalid choice. Please enter 1 or 0.")



        # Notifications
        notification_permission_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"))
        )
        notification_permission_btn.click()

        print("✅ Login flow completed.")

    except Exception as e:
        print(f"❌ Login flow failed: {e}")
