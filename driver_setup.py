# driver_setup.py
from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.support.ui import WebDriverWait

def get_driver():
    cap = {
        "platformName": "Android",
        "deviceName": "emulator-5554",
        "automationName": "UiAutomator2",
        "appPackage": "com.apnamart.apnaconsumer",
        "appActivity": "com.apnamart.apnaconsumer.presentation.activities.dashboard.DashBoardActivity",
    }

    url = 'http://127.0.0.1:4723'
    driver = webdriver.Remote(
        command_executor=url,
        options=AppiumOptions().load_capabilities(cap)
    )
    driver.implicitly_wait(5)
    return driver

def get_wait(driver):
    return WebDriverWait(driver, 10)
