import time
import querystar as qs
from pprint import pprint


data = qs.actions.slack.add_direct_message(
    user_id='U05M4EDS350',
    text=f'A message was sent by bot')
pprint(data)

raise SystemExit(0)
