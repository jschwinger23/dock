import os
import uuid
from abc import abstractmethod
from pathlib import Path


class Cgroups:
    def __init__(self, memory, cpushare):
        self.subsystems = [MemorySubsystem(memory), CPUSubsystem(cpushare)]

    def __enter__(self):
        for subsystem in self.subsystems:
            subsystem.apply()

    def __exit__(self, *args, **kws):
        for subsystem in self.subsystems:
            subsystem.destroy()


class Subsystem:
    def __init__(self, limit_value):
        self.limit_value = limit_value
        self.cgroup_name = uuid.uuid4().hex

    def apply(self):
        cgroup_path = self.mount_path / self.cgroup_name
        cgroup_path.mkdir()

        with (cgroup_path / self.limit_basename).open('a') as f:
            print(self.limit_value, file=f)
        with (cgroup_path / 'tasks').open('a') as f:
            print(os.getpid(), file=f)

    def destroy(self):
        root_task_path = self.mount_path / 'tasks'
        with root_task_path.open('a') as f:
            print(os.getpid(), file=f)

        cgroup_path = self.mount_path / self.cgroup_name
        cgroup_path.rmdir()

    @property
    def mount_path(self):
        return Path(self.mount_root)

    @property
    @abstractmethod
    def mount_root(self):
        ...

    @property
    @abstractmethod
    def limit_basename(self):
        ...


class MemorySubsystem(Subsystem):
    @property
    def mount_root(self):
        return '/sys/fs/cgroup/memory'

    @property
    def limit_basename(self):
        return 'memory.limit_in_bytes'


class CPUSubsystem(Subsystem):
    @property
    def mount_root(self):
        return '/sys/fs/cgroup/cpu'

    @property
    def limit_basename(self):
        return 'cpu.shares'
