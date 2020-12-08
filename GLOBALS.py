STACK_EXCHANGE_API_URL = "https://api.stackexchange.com/2.2/"
PER_SITE_METHOD = "search/advanced"
STACK_EXCHANGE_SITE = "stackoverflow"

"""STACKOVERFLOW API PARAMETER CUSTOMIZATION"""
PAGE_SIZE = 10

# can also be desc or asc
RESULTS_ORDER = "desc"

# can also be activity, votes, creation, relevance
RESULTS_SORT = "activity"

# REDIS SERVER
REDIS_HOST = "redis"
REDIS_PORT = 6379

# RATE LIMITING Info
PER_MIN_LIMIT = 5
PER_DAY_LIMIT = 100
