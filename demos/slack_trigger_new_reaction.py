import querystar as qs
from pprint import pprint


data = qs.triggers.slack.new_reaction(
    channel_id='C05M6QP7W92',
)
pprint(data)
