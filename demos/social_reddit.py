import querystar as qs
from pprint import pprint

data = qs.triggers.social.new_message(source='reddit')
pprint(data)