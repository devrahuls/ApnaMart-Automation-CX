from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def verify_offer_price_qty_inside_carts(driver, wait, expected_names_list, expected_added_count):
    #verify correct offer items has been added to cart with the correct offered qty and price
    """
    Verifies that the items successfully added from the bottomsheet are
    present in the cart and that the quantity matches the success count.
    """

    # Resource ID for product name in the cart (using user-specified string)
    CART_PRODUCT_NAME_ID = "product name"
    matched_count = 0

    print("\n--- Final Cart Verification ---")

    # Use a mutable list (copy of expected names) to track items we've matched and 'consumed'
    names_to_find = list(expected_names_list)

    try:
        # 1. Get all product name elements currently visible in the cart
        cart_product_elements = driver.find_elements(AppiumBy.ID, CART_PRODUCT_NAME_ID)

        if not cart_product_elements:
            print("❌ FAILED: No products found in the cart (Cart is empty).")
            raise AssertionError("Cart is unexpectedly empty.")

        # 2. Iterate through cart items and match against the expected list
        for cart_element in cart_product_elements:
            cart_name = cart_element.text.strip()

            # Check if this cart name exists in our list of expected names
            if cart_name in names_to_find:
                print(f"✅ MATCHED: Found '{cart_name}' in the cart.")
                matched_count += 1

                # 'Consume' the name to correctly handle duplicates (e.g., if Soap A was added twice)
                names_to_find.remove(cart_name)

                # 3. Final Comparison
        print(f"\nSummary: Expected={expected_added_count} | Found={matched_count}")

        if matched_count == expected_added_count:
            print(f"🎉 SUCCESS! Verified {matched_count} offer item(s) successfully added and reflecting in the cart.")
        else:
            print(f"❌ MISMATCH: Expected to find {expected_added_count} offer items, but only found {matched_count}.")

            if matched_count > expected_added_count:
                print("   -> WARNING: Found more matches than expected. Cart may contain duplicate residual items.")

            raise AssertionError(
                f"Cart verification failed. Count mismatch: Expected {expected_added_count}, Found {matched_count}.")

    except NoSuchElementException:
        print(f"❌ FAILED: Could not find any elements with ID '{CART_PRODUCT_NAME_ID}' on the cart page.")
        raise AssertionError("Cart verification failed: Cannot locate product names in cart.")