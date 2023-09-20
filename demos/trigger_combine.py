import time
import querystar as qs
from pprint import pprint

'''
data = qs.triggers.slack.new_message(
    channel_id='C05M6QP7W92',
)
data = qs.triggers.slack.new_reaction(
    channel_id='C05M6QP7W92',
)
'''

trigger_list = [
    (qs.triggers.slack.new_message, {
        'channel_id': 'C05M6QP7W92',
    }),
    (qs.triggers.slack.new_reaction, {
        'channel_id': 'C05M6QP7W92',
    }),
]

data = qs.triggers.combine(trigger_list)
pprint(data)
