import click
from uuid import uuid4
from querystar.client import ClientConnection


# Actions: with these 2 actions, we can replicate Gene's SAL9001 bot
# in the CTO Slacker
def add_message(channel_id: str,
                message: str,
                icon_emoji: str = '',
                icon_url: str = '',
                reply_broadcast: bool = False,
                thread_ts: str = ''):
    """
    All selected parameter's names match Slack http API arguments.
    HTTP API: https://api.slack.com/methods/chat.postMessage
    Scopes: chat:write, chat:write:user, chat:write:bot
    Rate limit: 1 per second, short burst ok, but no guarantee to send.
    """
    click.echo('Running:: actions.slack.add_message')
    _client_id = str(uuid4())
    _action_client = ClientConnection(
        integration='slack',
        event='add_message',
        client_id=_client_id)
    payload = {'channel': channel_id, 'text': message}
    data = _action_client.fire(payload)
    click.echo('Finished:: actions.slack.add_message')
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
    click.echo('Running:: actions.slack.find_message')
    _client_id = str(uuid4())
    _action_client = ClientConnection(
        integration='slack',
        event='find_message',
        client_id=_client_id)
    payload = {'query': query, 'count': count,
              'sort': sort, 'sort_direction': sort_direction}
    data = _action_client.fire(payload)
    click.echo('Finished:: actions.slack.find_message')
    return data
