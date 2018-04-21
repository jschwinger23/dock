import os
import ctypes
import ctypes.util
from typing import Tuple

STACK_SIZE = 8096

CLONE_NEWNS = 0x00020000
CLONE_NEWUTS = 0x04000000
CLONE_NEWIPC = 0x08000000
CLONE_NEWUSER = 0x10000000
CLONE_NEWPID = 0x20000000
CLONE_NEWNET = 0x40000000

SIGCHILD = 17


def pivot_root(new_root):
    new_root = new_root.rstrip('/')
    os.system(f'mount --bind {new_root} {new_root}')
    os.makedirs(f'{new_root}/.pivot', exist_ok=True)
    os.system(f'pivot_root {new_root} {new_root}/.pivot')
    os.chdir('/')
    os.system(f'umount -l /.pivot')
    os.rmdir('/.pivot')


def runc(image, commands: Tuple[str], tty: bool):
    def child_init():
        pivot_root(image)
        os.system('mount -t proc proc /proc')
        os.execv(commands[0], commands)
        return 0

    libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
    child_pid = libc.clone(
        ctypes.CFUNCTYPE(ctypes.c_int)(child_init),
        ctypes.c_char_p(
            ctypes.cast(ctypes.c_char_p(b' ' * STACK_SIZE), ctypes.c_void_p)
            .value + STACK_SIZE),
        CLONE_NEWUTS | CLONE_NEWIPC | CLONE_NEWPID | CLONE_NEWNS
        | CLONE_NEWNET | SIGCHILD)

    if child_pid < 0:
        errno = ctypes.get_errno()
        raise OSError(errno, f'Error run subprocess {commands}')
    else:
        os.waitpid(child_pid, 0)
