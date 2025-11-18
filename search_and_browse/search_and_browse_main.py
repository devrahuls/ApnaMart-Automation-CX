from search_and_browse.search_and_add_to_cart_flow import (search_and_add_to_cart_flow,
                                                           recent_searches, is_previously_bought_present,
                                                           previously_bought_view_all)

def search_and_browse_main(wait, item_name):
    search_and_add_to_cart_flow(wait, item_name)
    recent_searches(wait)
    is_previously_bought_present(wait)
    previously_bought_view_all(wait)
