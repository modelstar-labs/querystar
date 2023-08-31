import time
import querystar as qs
from pprint import pprint

time_now = str(time.time())
data = qs.actions.slack.add_message(
    channel_id='C05M6QP7W92',
    message=f'A repeat message was sent at {time_now}')
time.sleep(1)
