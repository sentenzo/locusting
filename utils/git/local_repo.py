from __future__ import annotations

import shutil
import os

from git import Git



class LocalRepositoryException(Exception):
    pass


class LocalRepository:
    def __init__(self, location: str, origin_url: str):
        if not LocalRepository.exists(location):
            LocalRepository.make_from_origin(location, origin_url)
        self.location = location
        self._git = Git(location)
        self._git_git = Git(os.path.join(location, ".git"))

    @staticmethod
    def exists(location):
        pass

    @staticmethod
    def make_from_origin(location: str, origin_url: str):
        if not os.path.exists(location):
            os.makedirs(location, exist_ok=True)
        if not os.path.isdir(location):
            raise LocalRepositoryException
        if len(os.listdir(location)) > 0:
            # not empty
            raise LocalRepositoryException

        _git = Git(location)
        _git.clone(origin_url, ".")

        _git_git = Git(os.path.join(location, ".git"))
        _git_git.init()
        _git_git.add(".")
        _git_git.commit(message="git-git")






    def duplicate(self, dup_location):
        shutil.copytree(self.location, dup_location)
        return LocalRepository(dup_location)

    def pull(self):
        pass

    def revert_pull(self):
        pass
