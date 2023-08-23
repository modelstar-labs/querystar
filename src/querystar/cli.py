import os
import click
import time
import types
import sys
from querystar.commands.run import compile_source_code, build_source_module


@click.group()
@click.version_option('0.1.0', message=f'\n{click.style("QueryStar", fg="magenta")}, installed version: {click.style("%(version)s", fg="magenta")}\n')
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

    try:
        while True:
            try:
                exec(bytecode, module.__dict__)
            except Exception as e:
                click.echo(f"Error executing '{e}' of type {type(e)}.")
                # TODO: Handle the following errors
                # <class 'ConnectionRefusedError'>
                # <class 'websockets.exceptions.ConnectionClosedError'>
                # TODO: Implement exponential retries
                break
            # time.sleep(1)
            # break
    except KeyboardInterrupt:
        click.echo(f"\n\nQueryStar stopped by user.\n")
        sys.exit(0)
