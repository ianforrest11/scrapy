from datetime import datetime, timedelta
import re

def iso_date(date_string):
    if any(char.isdigit() for char in date_string) == False:
        date_N_days_ago = datetime.now()
        return date_N_days_ago
    else:
        parsed_date = int(re.findall(r'\d+', date_string)[0])
        date_N_days_ago = datetime.now() - timedelta(days=parsed_date)
        return date_N_days_ago