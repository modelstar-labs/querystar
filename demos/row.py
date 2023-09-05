from time import time
from datetime import datetime
import querystar as qs
from pprint import pprint

time_now = str(time())
datetime_now = str(datetime.now())
data = qs.actions.google_sheets.add_row(
    spreadsheet_id='1OcgVHdMUWGEJhZd4dC4NscRNeFgVviCanMKp1o3XugI',
    worksheet_id='Sheet1',
    data=[[datetime_now, time_now, 'Hello World', 123456]]
)
pprint(data)