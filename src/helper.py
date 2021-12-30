import pytz
from datetime import datetime

api_sport_ids = {
    "PL": 39,
    "UCL": 2,
    "FA_CUP": 45,
    "LEAGUE_CUP": 48,
    "MANUTD": 33,
    "SAMPLE_FIXTURE": 710741
}

lineup_release_offset = {
    api_sport_ids["PL"]: 60,
    api_sport_ids["UCL"]: 75,
    api_sport_ids["FA_CUP"]: 60,
    api_sport_ids["LEAGUE_CUP"]: 60
}

# format example: 2021-12-30T20: 15: 00+00: 00
# should look into datetime.strptime
def to_datetime(timestamp:str):
    dt = timestamp.replace(' ', '')
    date = dt.split('T')[0]
    time = dt.split('T')[1]

    date = date.split('-')
    date = list(map(lambda d : int(d), date))

    time = [time.split(':')[0], time.split(':')[1]]
    time = list(map(lambda t : int(t), time))

    return datetime(date[0], date[1], date[2], time[0], time[1]).replace(tzinfo=pytz.UTC)


def min_item(compare_func, items:list):
    m_item = items[0]
    m_val = compare_func(m_item)
    
    for item in items:
        item_val = compare_func(item)
        if item_val < m_val:
            m_item = item
            m_val = item_val

    return m_item

def max_item(compare_func, items:list):
    m_item = items[0]
    m_val = compare_func(m_item)
    
    for item in items:
        item_val = compare_func(item)
        if item_val > m_val:
            m_item = item
            m_val = item_val

    return m_item