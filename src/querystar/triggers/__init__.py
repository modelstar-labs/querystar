import click
import time
from querystar.triggers import slack


def sleep_for(seconds: int = 0.1):
    """
    :param int seconds: trigger wait for `seconds` amount of time before returning
    """

    click.echo('Running:: triggers.sleep_for')
    click.echo('Finished:: triggers.sleep_for')
    time.sleep(seconds)
    return {'time_elapsed': 0.1}
