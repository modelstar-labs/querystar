import logging
from querystar.client import _client_connection

logger = logging.getLogger("querystar")



def add_direct_message(user_id: str,
                       text: str,
                       attachments: list = None,
                       blocks: list = None,
                       thread_ts: str = None,
                       reply_broadcast: bool = False,
                       icon_emoji: str = None,
                       icon_url: str = None):
    """
    All selected parameter's names match Slack http API arguments.
    HTTP API: https://api.slack.com/methods/conversations.open
    HTTP API: https://api.slack.com/methods/chat.postMessage
    HTTP API: https://api.slack.com/methods/chat.scheduleMessage
    Scopes: chat:write, chat:write:user, chat:write:bot
    Rate limit: 1 per second, short burst ok, but no guarantee to send.
    """
    logger.info('Started ACTION - slack.add_direct_message')
    # schedule_at
    # https://docs.google.com/spreadsheets/d/1qSGWVxSSHAde-HkzRy-mgjOGMR8k8N96jWAbHNUlOOk/edit#gid=181882786
    channel_id = ''
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
    add_message_data = _client_connection.fire(integration='slack',
                                               event='add_message',
                                               payload=payload)
    logger.info('Finished ACTION - slack.add_direct_message')
    return add_message_data
