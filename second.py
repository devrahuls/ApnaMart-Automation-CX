from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from time import sleep


# CAPABILITIES
cap = {
    "platformName": "Android",
    "deviceName": "emulator-5556",
    # "deviceName": "adb-ZA222VMD7F-VbfNR1._adb-tls-connect._tcp",
    # "deviceName":"ZA222VMD7F",
    "automationName": "UiAutomator2",
    "appPackage": "com.apnamart.apnaconsumer",
    "appActivity": "com.apnamart.apnaconsumer.presentation.activities.dashboard.DashBoardActivity",
}

# URL for the Appium Inspector
url = 'http://127.0.0.1:4723'

# Driver loading from the webdriver
driver = webdriver.Remote(
    command_executor=url,
    options=AppiumOptions().load_capabilities(cap))

# default wait time for any element to see on the screen
wait = WebDriverWait(driver, 10)



#AUTOMATION CODE

#Location permission access - press 'Yes' button
location_grant_access = WebDriverWait(driver, 10).until(
    lambda x: x.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_foreground_only_button")'
    )
)
location_grant_access.click()

#Pre-selected Language selection button on the login page
language_selection_button = WebDriverWait(driver, 3).until(
    lambda x: x.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/language_selection_button")'
    )
)
language_selection_button.click()


#If the user has truecaller installed then run this (OTP won't be asked in this process)
try:
    # ---------- TrueCaller login flow ----------

    truecallerConfirmBtn = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, "com.truecaller:id/tv_confirm"))
    )
    print("TrueCaller detected. Logging in via Truecaller...")
    truecallerConfirmBtn.click()

except TimeoutException:
    # ---------- Phone number + OTP login flow ----------

    print("TrueCaller not found. Logging in via phone number...")

    # Step 1: Find and click the phone input field to trigger any popups
    phone_input_field = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/phoneInputEditText"))
    )
    phone_input_field.click()

    # Step 2: Handle the "None of the above" autofill suggestion popup, if it appears
    try:
        none_of_above = WebDriverWait(driver, 3).until(
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
    # Now, send the phone number.
    sleep(0.5) #Pauses the execution of this script for 0.5 seconds.
    phone_input_to_fill.send_keys("9999999999")
    # driver.set_value(phone_input_to_fill, "9999999999")


    # Step 4: Click the "Continue" button
    continue_with_phone_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/continueWithPhone"))
    )
    continue_with_phone_btn.click()

    # Step 5: Enter the OTP
    enter_otp = wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")'))
    )
    enter_otp.send_keys("432967")



#Notification permission acceptance
notificationPermissionBtn = wait.until(
    EC.element_to_be_clickable((AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"))
)
notificationPermissionBtn.click()



#SEARCH - ADD TO CART
#Tap on the search bar
searchBarClick = wait.until(
    EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
)
searchBarClick.click()

searchInput = wait.until(
    EC.element_to_be_clickable((AppiumBy.ID, "com.apnamart.apnaconsumer:id/searchText"))
)
searchInput.send_keys("kurkure")

addFirstSearchedItem = wait.until(
    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddToCart").instance(0)'))
)
addFirstSearchedItem.click()

# Step 2: Handle the "Save Password to Google Password Manager" Bottom Sheet, if it appears
try:
    savePwdBtmShtNotNow = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/autofill_save_no")'))
    )
    savePwdBtmShtNotNow.click()
    print("Dismissed the 'Save Password to Google Password Manager' Bottom Sheet.")
except TimeoutException:
    print("No 'Save Password to Google Password Manager' Bottom Sheet appeared.")






# #Function to scroll down from the middle of the phone, till I find a particular text.
# def scroll_until_text(driver, text, max_swipes=25):
#     """
#     Scroll vertically from screen center until element with given text is found.
#     """
#     window_size = driver.get_window_size()
#     width = window_size["width"]
#     height = window_size["height"]
#
#     start_x = width // 2
#     start_y = int(height * 0.7)   # lower part of screen
#     end_y   = int(height * 0.3)   # upper part of screen
#
#     for i in range(max_swipes):
#         try:
#             el = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
#             return WebDriverWait(driver, 5).until(EC.visibility_of(el))
#         except NoSuchElementException:
#             # Swipe up
#             driver.swipe(start_x, start_y, start_x, end_y, 800)
#
#     raise Exception(f"Element with text '{text}' not found after {max_swipes} swipes")
#
# #Call the scroll down function and find the 'Freshener' word
# freshener = scroll_until_text(driver, "Fresheners")
#
# #Press the Add button to add the product on the cart
# add_to_cart_btn = wait.until(
#     EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.apnamart.apnaconsumer:id/btAddBig").instance(1)'))
# )
# add_to_cart_btn.click()
#
#view cart button
view_cart_btn = wait.until(
    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("View Cart")'))
)
view_cart_btn.click()

#select mop button
select_payment_mode_btn = wait.until(
    EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select Payment Mode")'))
)
select_payment_mode_btn.click()

#select COD radio option
select_payment_mode_cod = wait.until(
    EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cash On Delivery")'))
)
select_payment_mode_cod.click()

#select this payment and proceed with the button
select_payment_mode_confirm_btn = wait.until(
    EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button")'))
)
select_payment_mode_confirm_btn.click()

#place order button
place_order_btn = wait.until(
    EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Place Order")'))
)
place_order_btn.click()
