import querystar as qs
import time
from pprint import pprint

time_now = str(time.time())


data = qs.triggers.slack.new_message(
    channel_id='C05M6QP7W92',
    trigger_string='kudos')
pprint(data)
text_message = data.get('text', None)
data = qs.actions.slack.add_message(
    channel_id='C05LXN9BGKY',
    message=f'A kudos was sent at {time_now} with the text {text_message}')
print(data)
data = qs.actions.slack.find_message(query='kudos')
pprint(data)