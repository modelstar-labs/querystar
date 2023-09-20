import querystar as qs
from pprint import pprint

'''
{'event_ts': '1695032043.000600',
 'item': {'channel': 'C05M6QP7W92',
          'ts': '1695031109.732369',
          'type': 'message'},
 'item_user': 'U05M4EDS350',
 'reaction': 'tada',
 'type': 'reaction_added',
 'user': 'U05M4EDS350'}
'''

data = qs.triggers.slack.new_reaction(
    channel_id='C05M6QP7W92',
)
pprint(data)
