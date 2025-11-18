from offers_and_coupons.Best_Deals.best_deals_validation import best_deals_validate_main
from offers_and_coupons.Best_Deals.best_deals_verification import best_deals_verification


def best_deals_main(driver, wait):
    best_deals_verification(wait)
    best_deals_validate_main(driver, wait)