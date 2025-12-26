from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from global_variables import *

def upi_pending_page_verification(driver, wait):
    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_back'))
    )
    print('Back btn is displayed')

    page_heading = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/textView5'))
    )
    print(f'Page Heading with text : {page_heading.text}')

    wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/frameLayout'))
    )
    print(f'Countdown Box is Displaying')

    pay_within_text = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_pay_with_in'))
    )
    print(f' {pay_within_text.text} is Displaying')

    pay_within_time = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_pay_time'))
    )
    print(f'Pay Withing: {pay_within_time.text} Time is Displaying')

    how_to_pay_help_text = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_info'))
    )
    print(f'How To Pay Text: {how_to_pay_help_text.text} is Displaying')

    requested_upi = wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text({CORRECT_UPI}).text'))
    )
    print(f'Requested UPI: {requested_upi.text} is Displaying')

    page_caution_message = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/textView4'))
    )
    print(f'Page Caution Message: {page_caution_message.text} is Displaying')





















    pass

def cancel_txn_prompt(driver, wait):
    money_deduct_img = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/ic_close'))
    )
    print('')

    prompt_heading = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/heading'))
    )
    print(f'Prompt heading found with text : {prompt_heading.text}')

    prompt_subheading = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/subheading'))
    )
    print(f'Prompt Subheading found with text : {prompt_subheading.text}')

    yes_btn = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_yes'))
    )
    print(f'{yes_btn.text} Button found with text')

    no_btn = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_no'))
    )
    print(f'{no_btn.text} Button found with text')








    pass