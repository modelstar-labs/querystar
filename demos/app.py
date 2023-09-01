import time
import querystar as qs
from pprint import pprint

time_now = str(time.time())
data = qs.triggers.slack.new_message(
    channel_id='C05M6QP7W92',
    trigger_for_op_only=False,
    trigger_for_bot_messages=False,
)
pprint(data)
# message_ts = data['ts']
# user_id = data['user']
# user_text = data['text']
# data = qs.actions.slack.add_message(
#     channel_id='C05M6QP7W92',
#     text=f'A message was sent at {time_now} by {user_id} with the text {user_text}')
# pprint(data)
