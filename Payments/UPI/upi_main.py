import time

from selenium.common import NoSuchElementException

from cart_page.view_cart import view_cart
from offers_and_coupons.WholeSale.Helpers import add_more_products_to_unlock_wh_cart
from global_variables import *
from scroll_until_find_an_element import scroll_down_to_find_an_element
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from cart_page.place_order import save_address_and_assign_store_from_cart
from Payments.UPI.add_upi_address import add_upi_address, edit_upi_address
from Payments.UPI.upi_pending_page import upi_pending_page_verification, cancel_txn_prompt
from track_order_page import ongoing_track_order_page_verification
from cart_page.view_cart import view_cart
from Helpers import is_visible


def pay_using_view_verify(driver, wait):
    try:
        pay_using_view_component = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/pay_using_view'))
        )
        print('')

        back_btn_from_select_mop = wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(6)'))
        )
        back_btn_from_select_mop.click()
        print('')

        pay_using_arrow = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/pay_using_layout'))
        )
        print('')

        cart_total_payable_amt = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/cart_total_payable_amount'))
        )
        print('')

        payment_mode_box = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/card_payment_mode'))
        )
        print('')

        payment_mode_logo = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/icon'))
        )
        print('')

        payment_mode_text = wait.until(
            EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/payment_mode_text'))
        )
        print(f'{payment_mode_text.text}')






    except NoSuchElementException:
        print('❌ No Pay Using View has Found!')


def payment_failed_bottomsheet_verification(driver, wait):
    wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/img_cross'))
    )
    print('payment_failed_bottomsheet_img is displaying')

    title = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_payment_failed'))
    )
    print(f'Title : {title.text} , is displaying')

    subtitle = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_payment_failed_info'))
    )
    print(f'Payment Failed Info : {subtitle.text} , is displaying')

    retry_text = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_retry_payment'))
    )
    print(f'Retry text : {retry_text.text} , is displaying')

    pay_on_delivery_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_pay_on_delivery'))
    )
    print(f'{pay_on_delivery_btn.text} button, is displaying')

    retry_payment_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_retry_payment'))
    )
    print(f'{retry_payment_btn.text} button, is displaying')


def if_upi_already_exists(driver, wait):
    upi_id_list = wait.until(
        driver.find_elements((AppiumBy.XPATH, ''))
    )
    if len(upi_id_list) > 0:
        '''delete all the upi ids'''
        return True
    else:
        print('0 Pre-Saved UPI Ids Found, so Skipping the UPI ID Deletion')
        return False


def retry_payment_prompt_verification(driver, wait):
    pass


def payment_failed_higlight_track_order_page(driver, wait):
    payment_failed_icon = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/icon_pay_failed'))
    )
    print('payment_failed_icon is displaying')

    payment_failed_title = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/icon_pay_failed'))
    )
    print(f'Txn failed title : {payment_failed_title.text}')

    payment_failed_subtitle = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/tv_payment_failed_info'))
    )
    print(f'Txn failed subtitle : {payment_failed_subtitle.text}')




def upi_main(driver, wait):
    # add_more_products_to_unlock_wh_cart(driver, wait, MIN_AMT_REQUIRED_TO_PLACE_ORDER)
    view_cart(wait)

    to_pay = AppiumBy.ANDROID_UIAUTOMATOR
    to_pay_locator = 'new UiSelector().resourceId("to_pay")'
    scroll_down_to_find_an_element(driver, to_pay, to_pay_locator, 10)

    to_pay_amt = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("to_pay_amt")')))
    to_pay_amt = to_pay_amt.text

    if is_visible(driver,AppiumBy.ANDROID_UIAUTOMATOR ,'new UiSelector().text("Add Delivery Address")',timeout=2 ):
        save_address_and_assign_store_from_cart(driver, wait, STORE_ADDRESS)

    payment_mode_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select Payment Mode")'))
    )
    payment_mode_btn.click()

    # if upi id already exists then delete them all, that will verify the deletion process, so we can avoid this verification further
    is_deletion_skipped = if_upi_already_exists(driver, wait)

    add_upi_address(driver, wait, WRONG_UPI)

    pay_using_view = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/pay_using_view'))
    )
    pay_using_view.click()

    edit_upi_address(driver, wait)


    dont_delete_upi_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'com.apnamart.apnaconsumer:id/btn_cancel'))
    )
    dont_delete_upi_btn.click()

    select_and_proceed_upi = wait.until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(25)'))
    )
    select_and_proceed_upi.click()

    if(is_deletion_skipped == False):

        pay_using_view = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/pay_using_view'))
        )
        pay_using_view.click()

        check_saved_upi_address = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("haha@lala")'))
        )
        if (check_saved_upi_address.text == 'haha@lala'):
            print('LALALLALALA')

        edit_upi_address(driver, wait)

        dont_delete_upi_btn = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'com.apnamart.apnaconsumer:id/btn_cancel'))
        )
        dont_delete_upi_btn.click()

        # verify does the haha@lala upi id has successfully deleted by proving its not showing on screen
        upi_is_gone = wait.until(
            EC.invisibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("haha@lala")'))
        )
        if upi_is_gone:
            print("✅ Verified: The element has disappeared from the UI.")

        # add a new upi id - SECOND_WRONG_UPI
        add_upi_address(driver, wait, SECOND_WRONG_UPI)


    pay_using_view_verify(driver, wait)

    place_order_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/cart_button_layout'))
    )
    place_order_btn.click()
    time.sleep(5)

    payment_failed_bottomsheet_verification(driver, wait)

    retry_payment_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_retry_payment'))
    )
    retry_payment_btn.click()

    retry_payment_prompt_verification(driver, wait)
    time.sleep(4)

    payment_failed_bottomsheet_verification(driver, wait)

    payment_failed_bottomsheet_close_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/ic_close'))
    )
    payment_failed_bottomsheet_close_btn.click()

    pay_using_view_component = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/pay_using_view'))
    )
    pay_using_view_component.click()

    add_upi_address(driver, wait, CORRECT_UPI)

    place_order_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/cart_button_layout'))
    )
    place_order_btn.click()

    time.sleep(5)

    upi_pending_page_verification(driver, wait)

    back_btn_from_upi_pending_page = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_back'))
    )
    back_btn_from_upi_pending_page.click()

    cancel_txn_prompt(driver, wait)

    no_btn = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_no'))
    )
    no_btn.click()

    back_btn_from_upi_pending_page.click()

    yes_btn = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_yes'))
    )
    yes_btn.click()

    pay_on_delivery_btn = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, "com.apnamart.apnaconsumer:id/btn_pay_on_delivery"))
    )
    pay_on_delivery_btn.click()
    time.sleep(5)

    try:
        track_order_page_heading = wait.until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Track Order")'))
        )
        print(f'Successfully redirected to the {track_order_page_heading.text} page.')
    except NoSuchElementException:
        print('❌ Order was not get placed / Could not redirected to the Track Order page')

    # BEGIN PAY LATER PAYMENT FAILED VERIFICATION
    pay_later_btn = wait.until(
        EC.element_to_be_clickable((AppiumBy.ID, 'com.apnamart.apnaconsumer:id/btn_pay_now'))
    )
    print(f'{pay_later_btn.text} for the current order.')
    pay_later_btn.click()

    wrong_upi_option = wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text({WRONG_UPI})'))
    )
    wrong_upi_option.click()

    select_and_proceed_upi_option = wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select and Proceed (₹204)")'))
    )
    select_and_proceed_upi_option.click()

    payment_failed_higlight_track_order_page(driver, wait)

    if pay_later_btn.text == '':
        print('No Retry text found on Pay Now btn')

    pay_later_btn.click()


    correct_upi_option = wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text({CORRECT_UPI})'))
    )
    correct_upi_option.click()

    select_and_proceed_upi_option = wait.until(
        EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select and Proceed (₹204)")'))
    )
    select_and_proceed_upi_option.click()

    upi_pending_page_verification(driver, wait)

    back_btn_from_upi_pending_page.click()

    no_btn.click()

    back_btn_from_upi_pending_page.click()

    yes_btn.click()










































