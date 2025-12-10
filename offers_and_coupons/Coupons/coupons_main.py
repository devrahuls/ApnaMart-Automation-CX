from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

from offers_and_coupons.Coupons.coupon_verification import coupon_verification_main
from scroll_until_find_an_element import scroll_down_to_find_an_element, scroll_up_to_find_an_element



def coupons_main(driver, wait):

    coupon_verification_main(driver, wait)


