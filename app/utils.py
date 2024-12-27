from collections import defaultdict
from datetime import datetime

def count_customer(cart):
    return sum(int(c['number_customer']) for c in cart.values())


def year_month_day(time_string):
    dt = datetime.strptime(time_string, "%a, %d %b %Y %H:%M:%S %Z")
    return dt.strftime("%Y-%m-%d")


