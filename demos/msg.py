import time
import querystar as qs
from pprint import pprint


data = qs.actions.slack.add_message(
    channel_id='C05M6QP7W92',
    text=f'A message was sent by bot')
pprint(data)