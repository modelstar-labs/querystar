import time
import querystar as qs
from pprint import pprint

time_now = str(time.time())
data = qs.triggers.slack.new_message(
    # channel_id='C05M6QP7W92',
)
pprint(data)
message_ts = data['ts']
user_id = data['user']
user_text = data['text']
data = qs.actions.slack.find_user(user_id=user_id)
pprint(data)
data = qs.actions.slack.find_chat(channel_id='C05M6QP7W92', message_ts=message_ts)
pprint(data)
data = qs.actions.slack.add_message(
    channel_id='C05M6QP7W92',
    message=f'A message was sent at {time_now} by {user_id} with the text {user_text}')
pprint(data)
