import querystar as qs
from datetime import datetime
from pprint import pprint

data = qs.triggers.reddit.new_message('llm')
pprint(data)
# message_ts = data['ts']
# user_id = data['user']
# user_text = data['text']
# datetime_now = str(datetime.now())
# data = qs.actions.google_sheets.add_row(
#     spreadsheet_id='1OcgVHdMUWGEJhZd4dC4NscRNeFgVviCanMKp1o3XugI',
#     worksheet_id='Sheet1',
#     data=[[datetime_now, message_ts, user_id, user_text]]
# )