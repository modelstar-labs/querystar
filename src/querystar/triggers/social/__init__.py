import logging
from querystar.client import _client_connection

logger = logging.getLogger("querystar")


def new_message(source: str = None,
                channel_id: str = None,
                mentioned_user_id: str = None,
                trigger_string: str = None):
    """
    Listen for new messages in all social channels or a specific channel
    """
    logger.info('Subscribed TRIGGER - social.new_message')
    logger.info('Listening TRIGGER - social.new_message')

    filter_params = {
        'channel_id': channel_id,
        'mentioned_user_id': mentioned_user_id,
        'trigger_string': trigger_string,        
    }

    def filter_function(data: dict, filter_params: dict):        

        return True

    data = _client_connection.listen(integration='social',
                                     event=source,
                                     filter_function=filter_function,
                                     filter_params=filter_params)

    logger.info('Recieved TRIGGER - social.new_message')
    return data

