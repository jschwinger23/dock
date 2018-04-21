import click
from typing import Tuple

from .libs.runc import runc
from .libs.logging import getLogger

logger = getLogger(__name__)


@click.group()
def main():
    pass


@main.command('run')
@click.option('-i', '--iteractive', is_flag=True)
@click.option('-t', '--tty', is_flag=True)
@click.argument('commands', nargs=-1)
def run(iteractive: bool, tty: bool, commands: Tuple[str]):
    runc(commands, tty=tty)
