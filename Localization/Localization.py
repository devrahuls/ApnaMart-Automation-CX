from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def lang_change_from_profile_page(driver, wait):
    el1 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                              value="new UiSelector().className(\"android.widget.ImageView\").instance(2)")
    el1.click()
    el2 = driver.find_element(by=AppiumBy.ID, value="com.apnamart.apnaconsumer:id/changeLanguageMainHeading")
    el2.click()
    el3 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                              value="new UiSelector().resourceId(\"com.apnamart.apnaconsumer:id/language_radio_button\").instance(1)")
    el3.click()
    el4 = driver.find_element(by=AppiumBy.ID, value="com.apnamart.apnaconsumer:id/language_selection_button")
    el4.click()
    el5 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="वापस जाएं")
    el5.click()
