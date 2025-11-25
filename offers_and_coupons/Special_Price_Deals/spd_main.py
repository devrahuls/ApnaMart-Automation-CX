from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

from offers_and_coupons.Special_Price_Deals.spd_verification import spd_verification


def special_price_deals_main(driver, wait):
    spd_verification(driver, wait)
    pass
