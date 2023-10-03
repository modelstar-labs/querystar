import logging
from querystar.client import _client_connection

logger = logging.getLogger("querystar")


def new_message(keyword: str = None,
                trigger_string: str = None,
                author_user_id: str = None,
                sub_reddit: str = None):
    """
    Listen for new messages in in reddit with registered trigger string in your account.

    :param trigger_string: trigger if the message contains this string.
    :param author_user_id: trigger if the message is from this user id.
    :param sub_reddit: trigger if the message is from this subreddit.

    Returns: A dict containing the following keys:
    {
        "keyword": ...,
        "source": ...,
        "channel": ..,
        "type": ...,
        "user": ...,
        "text": ...,
        "ts": ...,
        "permalink": ...,
    }
    """
    logger.info('Subscribed TRIGGER - reddit.new_message')
    logger.info('Listening TRIGGER - reddit.new_message')

    filter_params = {
        'keyword': keyword,
        'trigger_string': trigger_string,
        'author_user_id': author_user_id,
        'sub_reddit': sub_reddit
    }

    def filter_function(data: dict, filter_params: dict):
        # Check for keyword
        filter_keyword = filter_params.get('keyword')
        if filter_keyword:
            keyword = data.get('keyword', None)
            if keyword:
                if filter_keyword != keyword:
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

        # Check for author_user_id
        filter_author_user_id = filter_params.get('author_user_id')
        if filter_author_user_id:
            author = data.get('user', None)
            if author:
                if filter_author_user_id != author:
                    return False
            else:
                return False

        # Check for sub_reddit
        filter_sub_reddit = filter_params.get('sub_reddit')
        if filter_sub_reddit:
            channel = data.get('channel', None)
            if channel:
                if filter_sub_reddit != channel:
                    return False
            else:
                return False

        return True

    data = _client_connection.listen(integration='social',
                                     event='reddit',
                                     filter_function=filter_function,
                                     filter_params=filter_params)

    logger.info('Recieved TRIGGER - reddit.new_message')
    return data
