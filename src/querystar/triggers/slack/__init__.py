import logging
from querystar.client import _client_connection

logger = logging.getLogger("querystar")


def new_message(channel_id: str = None,
                mentioned_user_id: str = None,
                trigger_string: str = None,
                trigger_for_bot_messages: bool = False,
                trigger_for_op_only: bool = False):
    """
    :param str channel_id: trigger if event['channel'] matches the given channel
    :param str mentioned_user_id: trigger if event['user'] matches the given user id.
    :param str trigger_string: only triggered if message's text include the given string
            Note: 
            1) if non of the above 3 parameters are given, trigger by every message
            2) if 2 or 3 parameters are given, trigger logic should be trigger_1 AND trigger_2
    :param bool trigger_for_bot_messages: whether triggered by messages sent by a bot
            Note for implementation: 
            1) all parameters need custom logic. channel_id's priority should be the highest. 
            The others can wait.
            2) We need to subscribe to both public channel and private channel
            Public channel message API: https://api.slack.com/events/message.channels
            Private channel message API: https://api.slack.com/events/message.groups
    : param bool trigger_for_op_only: whether triggered by original post only    

    Scopes: channels:history, groups:history
    """
    logger.info('Subscribed TRIGGER - slack.new_message')
    logger.info('Listening TRIGGER - slack.new_message')

    filter_params = {
        'channel_id': channel_id,
        'mentioned_user_id': mentioned_user_id,
        'trigger_string': trigger_string,
        'trigger_for_bot_messages': trigger_for_bot_messages,
        'trigger_for_op_only': trigger_for_op_only
    }

    def filter_function(data: dict, filter_params: dict):
        # Check for channel_id
        filter_channel_id = filter_params.get('channel_id')
        if filter_channel_id:
            channel_id = data.get('channel', None)
            if channel_id:
                if data['channel'] != filter_channel_id:
                    return False
            else:
                return False

        # Check for mentioned_user_id
        filter_mentioned_user_id = filter_params.get('mentioned_user_id')
        if filter_mentioned_user_id:
            text = data.get('text', None)
            if text:
                if filter_mentioned_user_id not in text:
                    return False
            else:
                return False

        # Check for trigger_string
        filter_trigger_string = filter_params.get('trigger_string')
        if filter_trigger_string:
            text = data.get('text', None)
            if text:
                if filter_trigger_string not in text:
                    return False
            else:
                return False

        # Check for trigger_for_bot_messages
        # if trigger_for_bot_messages = False => if_bot => return False
        # if trigger_for_bot_messages = True => if_bot => return True
        filter_trigger_for_bot_messages = filter_params.get(
            'trigger_for_bot_messages')
        if not filter_trigger_for_bot_messages:
            # check user info
            user_id = data.get('user', None)
            if user_id:
                payload = {'user': user_id}
                _user_data = _client_connection.fire(integration='slack',
                                                     event='find_user',
                                                     payload=payload)
                user_info = _user_data.get('user', None)
                if user_info:
                    if user_info['is_bot']:
                        return False
                else:
                    return False
            else:
                return False

        # Check for orignial post message only
        # if trigger_for_op_only = False => return True
        # if trigger_for_op_only = True => if original post => return True
        filter_trigger_for_op_only = filter_params.get('trigger_for_op_only')
        if filter_trigger_for_op_only:
            # a reply will have thread_ts, for original post thread_ts = None
            thread_ts = data.get('thread_ts', None)
            if thread_ts:
                return False

        return True

    data = _client_connection.listen(integration='slack',
                                     event='new_message',
                                     filter_function=filter_function,
                                     filter_params=filter_params)

    logger.info('Recieved TRIGGER - slack.new_message')
    return data


def new_reaction(channel_id: str = None,
                 message_ts: str = None,
                 reaction: str = None,
                 user_id: str = None,
                 trigger_for_message_only=True):
    """
    :param str channel_id: trigger if event['item']['channel'] matches the given channel
    :param str message_ts: trigger if event['item']['ts'] matches the given ts
    :param str reaction: trigger if event['reaction'] matches the given reaction str, e.g. 'thumbup'.
    :param str user_id: trigger if event['user'] matches the given user id
    :param bool trigger_for_message_only: when this is set to True, trigger if event['item']['type']=='message'

    Note: 
    All filters are composited using 'AND' logic
    Reaction_added event message API: https://api.slack.com/events/reaction_added
    Scopes: reactions:read
    """
    pass
