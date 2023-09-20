import time
import querystar as qs
from pprint import pprint


data = qs.actions.slack.add_message(
    channel_id='C05M6QP7W92',
    text=f'The big kudos message of all time!')
pprint(data)
data = qs.actions.slack.find_message(query='big kudos')
pprint(data)
data = qs.actions.slack.find_permalink(
    channel_id='C05M6QP7W92',
    message_ts='1695031109.732369')
pprint(data)
data = qs.actions.slack.find_user(user_id='U05M4EDS350')
pprint(data)
data = qs.actions.slack.find_thread(
    channel_id='C05M6QP7W92',
    thread_ts='1695031109.732369')
pprint(data)

raise ValueError('Stop here')