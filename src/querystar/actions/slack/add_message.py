import logging
from querystar.client import _client_connection

logger = logging.getLogger("querystar")


def add_message(channel_id: str,
                text: str = None,
                attachments: list = None,
                blocks: list = None,
                thread_ts: str = None,
                reply_broadcast: bool = False,
                icon_emoji: str = None,
                icon_url: str = None):
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
    if thread_ts is not None:
        payload['thread_ts'] = thread_ts
    if icon_emoji is not None:
        payload['icon_emoji'] = icon_emoji
    if icon_url is not None:
        payload['icon_url'] = icon_url

    data = _client_connection.fire(integration='slack',
                                   event='add_message',
                                   payload=payload)
    logger.info('Finished ACTION - slack.add_message')
    return data
