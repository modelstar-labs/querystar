from datetime import datetime
import querystar as qs


data = qs.triggers.slack.new_message(
    channel_id='C05RXSVC5F0',  # sheets-demo
    trigger_for_op_only=False,
    trigger_for_bot_messages=False,
)
message_ts = data['ts']
user_id = data['user']
user_text = data['text']
datetime_now = str(datetime.now())
data = qs.actions.google_sheets.add_row(
    spreadsheet_id='1OcgVHdMUWGEJhZd4dC4NscRNeFgVviCanMKp1o3XugI',
    worksheet_id='Sheet1',
    data=[[datetime_now, message_ts, user_id, user_text]]
)
