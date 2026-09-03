from datetime import datetime

def convert_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()

def convert_datetime(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

def convert_boolean(value):
    value = value.strip().lower()
    if value == "true":
        return True
    elif value == "false":
        return False
    raise ValueError