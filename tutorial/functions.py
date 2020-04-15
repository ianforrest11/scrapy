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
    
    
def parse(x):
    shape = {"job_id": x.get("job_id")[0],
            'job_position': x.get("job_position")[0],
            'company_name': x.get("company_name")[0],
            'job_location': x.get("job_location")[0],
            'job_salary': x.get("job_salary")[0],
            'job_description': x.get("job_description")[0],
            'published_at': x.get("published_at")[0],
            'application_link': x.get("application_link"),
            'source': x.get("source")}
    return shape