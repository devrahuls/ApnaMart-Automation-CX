from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait

from scroll_until_find_an_element import scroll_down_to_find_an_element

def spd_verification(driver, wait):

    # Scroll until we find the SPD Offer
    target_element = "com.apnamart.apnaconsumer:id/btn_add_products"
    scroll_down_to_find_an_element(driver, AppiumBy.ID, target_element, 10)

    # verify the whole single sku deals offer
    try:
        wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/single_sku_deals"))
        )
        print("✅ Single SKU Deals / Special Price Deals component is visible.")
    except TimeoutException:
        print("❌ Single SKU Deals / Special Price Deals component is NOT visible.")

    # verify the offer heading
    try:
        spd_offer_heading = wait.until(
            EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Special Price Deals")'))
        )
        print(f'✅ {spd_offer_heading.text} offer heading is available')
    except NoSuchElementException:
        print('❌ Best Deals offer heading is not available')

