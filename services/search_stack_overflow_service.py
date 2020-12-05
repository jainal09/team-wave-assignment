import requests
from GLOBALS import STACK_EXCHANGE_API_URL, STACK_EXCHANGE_SITE, PER_SITE_METHOD, PAGE_SIZE, RESULTS_ORDER, RESULTS_SORT


def search_stack_over_flow(question, page):
    url = STACK_EXCHANGE_API_URL + PER_SITE_METHOD + "?page=" + str(page) + \
          "&pagesize=" + str(PAGE_SIZE) + "&order=" + RESULTS_ORDER + "&sort=" + RESULTS_SORT + \
          "&q=" + question + "&site=" + STACK_EXCHANGE_SITE
    print(url)
    try:
        response = requests.request("GET", url)
        data = response.json()
        if not data["has_more"]:
            """no more pages"""
            return None
        elif data["quota_remaining"] == 0:
            """quota completed"""
            return None
        else:
            return data
    except Exception as stack_api_error:
        print(stack_api_error)
        return None
