import click
from typing import Tuple

from psutil import virtual_memory

from .libs.runc import runc
from .libs.cgroups import Cgroups
from .libs.logging import getLogger

logger = getLogger(__name__)


@click.group()
def main():
    pass


@main.command('run')
@click.option('-i', '--iteractive', is_flag=True)
@click.option('-t', '--tty', is_flag=True)
@click.option('-m', '--memory', type=str, default=virtual_memory().total)
@click.option('-cpu', '--cpushare', type=int, default=1024)
@click.argument('commands', nargs=-1)
def run(iteractive: bool, tty: bool, memory: str, cpushare: str,
        commands: Tuple[str]):
    with Cgroups(memory=memory, cpushare=cpushare):
        runc(commands, tty)
