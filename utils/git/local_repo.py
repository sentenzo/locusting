from __future__ import annotations

import shutil
from os import path

from git import Git


class LocalRepository:
    def __init__(self, location: str, origin_url: str):
        if not LocalRepository.exists(location):
            LocalRepository.make_from_origin(location, origin_url)
        self.location = location
        self.repo_git = Git(location)
        self.git_git = Git(path.join(location, ".git"))

    @staticmethod
    def exists(location):
        ...

    @staticmethod
    def make_from_origin(location: str, origin_url: str):
        ...

    def duplicate(self, dup_location):
        shutil.copytree(self.location, dup_location)
        return LocalRepository(dup_location)

    def pull(self):
        pass

    def revert_pull(self):
        pass

    # git.cmd
    # https://stackoverflow.com/questions/2472552/python-way-to-clone-a-git-repository
    # https://stackoverflow.com/questions/15315573/how-can-i-call-git-pull-from-within-python
    # https://stackoverflow.com/questions/28291909/gitpython-and-ssh-keys
