import time
import querystar as qs
from pprint import pprint

time_now = str(time.time())
data = qs.actions.slack.add_message(
    channel_id='C05M6QP7W92',
    message=f'A message was sent at {time_now} by bot-add-message.py')
pprint(data)

raise Exception('Done')
