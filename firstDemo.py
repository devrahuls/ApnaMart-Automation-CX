from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# cap: Dict[str, Any] = {
#     "platformName": "Android",
#     "deviceName": "emulator-5554",
#     "automationName": "UiAutomator2",
#     "appPackage": "com.android.settings",
#     "appActivity": ".Settings",
#     "language" : 'en',
# }

cap = {
    "platformName": "Android",
    "deviceName": "emulator-5554",
    "automationName": "UiAutomator2",
    "appPackage": "com.android.chrome",
    "appActivity": "com.google.android.apps.chrome.Main"
}

url = 'http://127.0.0.1:4723'

driver = webdriver.Remote(
    command_executor=url,
    options=AppiumOptions().load_capabilities(cap))

# print(driver.page_source)

# el = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Battery")')
# el.click()

# driver.find_element(
#     AppiumBy.ANDROID_UIAUTOMATOR,
#     'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains("Battery"))'
# ).click()

# driver.find_element(
#     AppiumBy.ANDROID_UIAUTOMATOR,
#     'new UiSelector().text("Chrome")'
# ).click()

# driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Chrome").click()



# driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Chrome").click()
# new UiSelector().text("Chrome")

# driver.find_element(
#     AppiumBy.ANDROID_UIAUTOMATOR,
#     'new UiSelector().resourceId("com.android.chrome:id/search_box_text")'
# ).send_keys("Hello")

# driver.find_element(
#     AppiumBy.ACCESSIBILITY_ID,
#     'com.android.chrome:id/signin_fre_continue_button'
# ).click()


driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.android.chrome:id/signin_fre_continue_button")'
).click()

positive_button = WebDriverWait(driver, 10).until(
    lambda x: x.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.android.chrome:id/positive_button")'
    )
)
positive_button.click()


yes_iam_in = WebDriverWait(driver, 10).until(
    lambda x: x.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.android.chrome:id/button_primary")'
    )
)
yes_iam_in.click()

ack_button = WebDriverWait(driver, 10).until(
    lambda x: x.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.android.chrome:id/ack_button")'
    )
)
ack_button.click()

search_box = WebDriverWait(driver, 10).until(
    lambda x: x.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.android.chrome:id/search_box_text")'
    )
)

search_box.send_keys('Hello')