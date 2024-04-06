import pytz


def to_name(t):
    return t.replace("/", "_").replace("-", "_MIN_").replace("+", "_PLUS_").upper()


timezones = {to_name(tz): tz for tz in pytz.all_timezones}
