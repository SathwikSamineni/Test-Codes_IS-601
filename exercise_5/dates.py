from datetime import datetime, date, timedelta

def my_datetime(dt):
    return dt.strftime("%Y %m %d %H %M %S")

def saturdays():
    today = date.today()
    jan_1_next_year = date(today.year + 1, 1, 1)
    
    days_ahead = 5 - today.weekday()
    if days_ahead < 0:
        days_ahead += 7
    
    next_saturday = today + timedelta(days=days_ahead)
    saturdays_list = []
    
    while next_saturday < jan_1_next_year:
        saturdays_list.append(next_saturday)
        next_saturday += timedelta(weeks=1)
    
    return saturdays_list

def first_or_fifteenth(d):
    if d.day == 1 or d.day == 15:
        if d.weekday() not in (5, 6):
            return True
    return False
