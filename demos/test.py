import time
import querystar as qs
from pprint import pprint

time_now = str(time.time())
data = qs.triggers.slack.new_message(
    trigger_for_bot_messages=True
)
message_ts = data['ts']
user_id = data['user']
user_text = data['text']
print(f'Msg rcvs {user_text} ts of {message_ts}')
time.sleep(2)
