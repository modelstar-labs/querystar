import click
from querystar.client import ClientConnection
from uuid import uuid4

# Events = triggers. This one trigger can cover lots of user cases already.
# Let's start with it


def new_message(channel_id: str = None,
                mentioned_user_id: str = None,
                trigger_string: str = None,
                trigger_for_bot_messages: bool = False):
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

    Scopes: channels:history, groups:history
    """
    click.echo('Running:: triggers.slack.new_message')
    _client_id = str(uuid4())
    _trigger_client = ClientConnection(
        integration='slack',
        event='new_message',
        client_id=_client_id)

    filter_params = {
        'channel_id': channel_id,
        'mentioned_user_id': mentioned_user_id,
        'trigger_string': trigger_string,
        'trigger_for_bot_messages': trigger_for_bot_messages
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

        return True

    data = _trigger_client.listen(
        filter_function=filter_function,
        filter_params=filter_params)

    click.echo('Finished:: triggers.slack.new_message')
    return data
