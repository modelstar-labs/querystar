import logging
from querystar.client import _client_connection

logger = logging.getLogger("querystar")


def add_message(channel_id: str,
                text: str = None,
                attachments: list = None,
                blocks: list = None,
                thread_ts: str = '',
                reply_broadcast: bool = False,
                icon_emoji: str = '',
                icon_url: str = ''):
    """
    All selected parameter's names match Slack http API arguments.
    HTTP API: https://api.slack.com/methods/chat.postMessage
    Scopes: chat:write, chat:write:user, chat:write:bot
    Rate limit: 1 per second, short burst ok, but no guarantee to send.
    """
    logger.info('Started ACTION - slack.add_message')
    payload = {'channel': channel_id,
               'reply_broadcast': reply_broadcast}
    if text is not None:
        payload['text'] = text
    if attachments is not None:
        payload['attachments'] = attachments
    if blocks is not None:
        payload['blocks'] = blocks

    if thread_ts != '':
        payload['thread_ts'] = thread_ts
    data = _client_connection.fire(integration='slack',
                                   event='add_message',
                                   payload=payload)
    logger.info('Finished ACTION - slack.add_message')
    return data


def find_user(user_id: str):
    """
    All selected parameter's names match Slack http API arguments.
    HTTP API: https://api.slack.com/methods/users.info
    Scopes: users:read    
    """
    logger.info('Started ACTION - slack.find_user')
    payload = {'user': user_id}
    data = _client_connection.fire(integration='slack',
                                   event='find_user',
                                   payload=payload)
    logger.info('Finished ACTION - slack.find_user')
    return data


def find_permalink(channel_id: str, message_ts: str):
    """
    All selected parameter's names match Slack http API arguments.
    HTTP API: https://api.slack.com/methods/chat.getPermalink
    Scopes: None
    """
    logger.info('Started ACTION - slack.find_permalink')
    payload = {'channel': channel_id, 'message_ts': message_ts}
    data = _client_connection.fire(integration='slack',
                                   event='find_permalink',
                                   payload=payload)
    logger.info('Finished ACTION - slack.find_permalink')
    return data


def find_message(query: str,
                 count: int = 20,
                 sort: str = 'score',
                 sort_direction: str = 'desc'):
    """
    All selected parameter's names match Slack http API arguments.
    HTTP API: https://api.slack.com/methods/search.messages
    Scopes: search:read
    Rate limit: 20+ per minute, occasional busts ok, ideally <50
    """
    logger.info('Started ACTION - slack.find_message')
    payload = {'query': query, 'count': count,
               'sort': sort, 'sort_dir': sort_direction}
    data = _client_connection.fire(integration='slack',
                                   event='find_message',
                                   payload=payload)
    logger.info('Finished ACTION - slack.find_message')
    return data
