from datetime import datetime, timedelta
import re

def iso_date(date_string):
    if any(char.isdigit() for char in date_string) == False:
        date_N_days_ago = datetime.now().date()
        return date_N_days_ago
    else:
        parsed_date = int(re.findall(r'\d+', date_string)[0])
        date_N_days_ago = datetime.now().date() - timedelta(days=parsed_date)
        return date_N_days_ago
    

def remove_unwanted(value):
    x = value.replace(u'\n', "")
    x = value.replace(u'\n ', "")
    x = x.lstrip()
    return x