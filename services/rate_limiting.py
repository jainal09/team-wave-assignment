import datetime
from .redis_cache_helper_service import set_cache, get_cache
from GLOBALS import PER_MIN_LIMIT, PER_DAY_LIMIT


# Rate Limiting logic
def limiter(request):
    now = datetime.datetime.now()
    current_minute = now.year + now.month + now.day + now.hour + now.minute
    current_date = now.year + now.month + now.day
    # get ip to identify clients uniquely
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        print(ip)
    else:
        ip = request.META.get('REMOTE_ADDR')
        print(ip)
    # get per minute counts of request of this client from redis
    min_count = get_cache(ip, current_minute)
    print("min_count", str(min_count))
    day_count = get_cache(ip, current_date)
    print("day_count", str(day_count))
    if day_count is None and min_count is None:
        print("in day NONE and min NONE")
        day_count = 1
    # initialize and set per minute and day count of request of this client
        set_cache(ip, current_date, day_count)
        min_count = 1
        set_cache(ip, current_minute, min_count)
        return False
    elif min_count is None and day_count is not None:
        print("min NONe and day not None")
        if day_count > PER_DAY_LIMIT - 1:
            return True
        else:
            min_count = 1
            set_cache(ip, current_minute, min_count)
            set_cache(ip, current_date, day_count + 1)
            # Check if per minute and day count of request of this client exceeds limits
            return False
    elif min_count is not None and day_count is not None:
        print("min not None and day not none")
        if min_count > PER_MIN_LIMIT - 1 or day_count > PER_DAY_LIMIT - 1:
            return True
        else:
            set_cache(ip, current_minute, min_count + 1)
            set_cache(ip, current_date, day_count + 1)
            return False
