import util
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Directory:
    parent: Optional["Directory"]
    name: str
    size: int = 0
    sub_directories: List["Directory"] = field(default_factory=list)

    def has_sub_directory(self, name: str):
        return any(name == d.name for d in self.sub_directories)

    def get_sub_directory(self, name: str):
        for d in self.sub_directories:
            if d.name == name:
                return d
        raise Exception("Parsing error")


root = Directory(None, "/")
cwd = root

for line in util.read_lines("inputs/day7.txt"):
    cmds = line.split(" ")
    match cmds:
        case "$", "cd", "/":
            cwd = root
        case "$", "cd", "..":
            assert cwd.parent
            cwd = cwd.parent
        case "$", "cd", sub_dir_name:
            cwd = cwd.get_sub_directory(sub_dir_name)
        case "$", "ls":
            continue
        case "dir", dir_name:
            assert not cwd.has_sub_directory(dir_name)
            cwd.sub_directories.append(Directory(cwd, dir_name))
        case size, file_name:
            cwd.size += int(size)


def dfs(directory: Directory, set_closest=False):
    global closest_dir_size
    total = directory.size
    for sub in directory.sub_directories:
        total += dfs(sub, set_closest)
    if set_closest and total >= space_needed:
        closest_dir_size = min(closest_dir_size, total)
    return total


total_size = dfs(root)
space_needed = 30000000 - (70000000 - total_size)
closest_dir_size = 70000000
dfs(root, True)
print(closest_dir_size)
