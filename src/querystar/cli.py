import os
import click
import time
import types
import sys
import logging
from websockets.exceptions import ConnectionClosedError
from querystar.commands.run import compile_source_code, build_source_module
from querystar.exceptions import BadRequestException, UnauthorizedException
from querystar.settings import settings
from querystar.logger import initialize_logger


@click.group()
@click.version_option('0.3.8', message=f'\n{click.style("QueryStar", fg="magenta")}, installed version: {click.style("%(version)s", fg="magenta")}\n')
@click.pass_context
def main(ctx):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)

    ctx.ensure_object(dict)

    ctx.obj['env'] = 'dev'


@main.command("run")
@click.argument("target", required=True, type=click.Path(exists=True))
@click.option("--rl", is_flag=True, show_default=True, default=False, help="Remote logging.")
@click.pass_context
def run(ctx, target: str, rl: bool):
    '''
    querystar run tests/app.py
    '''

    target_path = os.path.abspath(target)
    bytecode = compile_source_code(target_path)
    module = build_source_module(target_path)
    _connection_retry_times = 0

    app_id = os.path.basename(target_path).split(".")[0]
    settings.set_app_id(app_id)

    initialize_logger(rl)

    logger = logging.getLogger("querystar")
    logger.info(f"QueryStar running {target} (Press CTRL+C to quit)")
    logger.info('Finished ACTION - slack.add_message')

    try:
        while True:
            try:
                # Add the folder of the file into exec context to add local imports
                sys.path.append(os.path.dirname(target_path))
                exec(bytecode, module.__dict__)
                _connection_retry_times = 0
            except BadRequestException as e:
                raise e
            except UnauthorizedException as e:
                raise e
            except ConnectionClosedError:
                logger.info("QueryStar stopped by server. Reconnecting...")
                # TODO: Implement exponential retries
                _connection_retry_times += 1
                if _connection_retry_times > 10:
                    logger.error("Reconnect limit exceeded.")
                    logger.error(
                        "Server unresponsive, contact QuerStar support.")
                    sys.exit(0)
                else:
                    time.sleep(1*(_connection_retry_times+1))
            except ConnectionRefusedError:
                logger.info(f"QueryStar stopped by server. Reconnecting...")
                # TODO: Implement exponential retries
                _connection_retry_times += 1
                if _connection_retry_times > 10:
                    logger.error("Reconnect limit exceeded.")
                    logger.error(
                        "Server unresponsive, contact QuerStar support.")
                    sys.exit(0)
                else:
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Error executing '{e}' of type {type(e)}.")
                sys.exit(0)
            # time.sleep(1)
            # break
    except KeyboardInterrupt:
        logger.info(f"QueryStar stopped by user.")
        sys.exit(0)
