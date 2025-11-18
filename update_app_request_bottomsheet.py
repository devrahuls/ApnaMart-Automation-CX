
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


def remove_update_app_bottomsheet(driver):

    wait = WebDriverWait(driver, 5)

    # If Update app request bottomsheet appears
    try:
        update_heading_id = wait.until(
            EC.visibility_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/updateHeading"))
        )

        # 3. If the wait succeeds, the heading exists. Now click the 'Later' button.
        print(f"Update - {update_heading_id.text} popup found. Clicking 'Skip' button.")

        skip_button_id = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btnLater'))
        )
        skip_button_id.click()

    except TimeoutException:
        # 4. If the wait times out, the heading was not found.
        #    This is the "else" case: we do nothing and just continue.
        print("Update popup not found. Continuing script.")
        pass