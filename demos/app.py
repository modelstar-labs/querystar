import querystar as xa
from pprint import pprint


data = xa.triggers.slack.new_message()
pprint(data)
data = xa.actions.slack.user_info(user_id=data['user'])
pprint(data)
