import os
import click
import time
import types
import sys
from querystar.commands.run import compile_source_code, build_source_module
from querystar.exceptions import BadRequestException, UnauthorizedException
from websockets.exceptions import ConnectionClosedError


@click.group()
@click.version_option('0.3.2', message=f'\n{click.style("QueryStar", fg="magenta")}, installed version: {click.style("%(version)s", fg="magenta")}\n')
@click.pass_context
def main(ctx):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)

    ctx.ensure_object(dict)

    ctx.obj['env'] = 'dev'


@main.command("run")
@click.argument("target", required=True, type=click.Path(exists=True))
@click.pass_context
def run(ctx, target: str):
    '''
    querystar run tests/app.py
    '''

    click.echo(f"\nRunning {target}\n")

    target_path = os.path.abspath(target)
    bytecode = compile_source_code(target_path)
    module = build_source_module(target_path)
    _connection_retry_times = 0

    try:
        while True:
            try:
                exec(bytecode, module.__dict__)
                _connection_retry_times = 0
            except BadRequestException as e:
                raise e
            except UnauthorizedException as e:
                raise e
            except ConnectionClosedError:
                click.echo(
                    f"QueryStar stopped by server. Reconnecting...")
                # TODO: Implement exponential retries
                _connection_retry_times += 1
                if _connection_retry_times > 10:
                    click.echo("Reconnect limit exceeded.")
                    click.echo(
                        "Server unresponsive, contact QuerStar support.")
                    sys.exit(0)
                else:
                    time.sleep(1*(_connection_retry_times+1))
            except ConnectionRefusedError:
                click.echo(f"QueryStar stopped by server. Reconnecting...")
                # TODO: Implement exponential retries
                _connection_retry_times += 1
                if _connection_retry_times > 10:
                    click.echo("Reconnect limit exceeded.")
                    click.echo(
                        "Server unresponsive, contact QuerStar support.")
                    sys.exit(0)
                else:
                    time.sleep(1)
            except Exception as e:
                click.echo(f"Error executing '{e}' of type {type(e)}.")
                sys.exit(0)
            # time.sleep(1)
            # break
    except KeyboardInterrupt:
        click.echo(f"\n\nQueryStar stopped by user.\n")
        sys.exit(0)
