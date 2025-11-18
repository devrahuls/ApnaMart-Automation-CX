from offers_and_coupons.WholeSale.wholesale_verification import wholesale_verification
from search_and_browse.search_and_add_to_cart_flow import search_and_add_to_cart_flow
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy


def wholesale_main(wait):
    search_and_add_to_cart_flow(wait, "lux ulitmate")
    verify_tag = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/vip_offer_layout'))
    )
    wholesale_verification(wait)