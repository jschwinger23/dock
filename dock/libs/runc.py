import os
import ctypes

CLONE_NEWNS = 0x00020000
CLONE_NEWUTS = 0x04000000
CLONE_NEWIPC = 0x08000000
CLONE_NEWUSER = 0x10000000
CLONE_NEWPID = 0x20000000
CLONE_NEWNET = 0x40000000
SIGCHILD = 17


def runc(command: str, tty: bool):
    commands = command.split()

    def child_init():
        os.system('mount -t proc proc /proc')
        os.execv(commands[0], commands)
        return 0

    child_init = ctypes.CFUNCTYPE(ctypes.c_int)(child_init)
    child_stack = ctypes.c_char_p(b' ' * 8096)
    child_stack = ctypes.c_void_p(
        ctypes.cast(child_stack, ctypes.c_void_p).value + 8096)

    libc = ctypes.CDLL('libc.so.6')
    child_pid = libc.clone(
        child_init, child_stack,
        CLONE_NEWUTS | CLONE_NEWIPC | CLONE_NEWPID | CLONE_NEWNS
        | CLONE_NEWNET | SIGCHILD)
    os.waitpid(child_pid, 0)
