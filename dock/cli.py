import click

from .libs.runc import runc
from .libs.logging import getLogger

logger = getLogger(__name__)


@click.group()
def main():
    pass


@main.command('run')
@click.option('-i', '--iteractive', is_flag=True)
@click.option('-t', '--tty', is_flag=True)
@click.argument('command')
def run(iteractive: bool, tty: bool, command: str):
    runc(command, tty=tty)
