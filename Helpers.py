from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
import time


def is_visible(driver, locator_type, locator_value, timeout=1):
    """Checks if an element is visible within a short timeout without throwing an error."""
    try:
        # Use presence_of_element_located for quick check
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((locator_type, locator_value))
        )
        return True
    except (TimeoutException, NoSuchElementException):
        return False