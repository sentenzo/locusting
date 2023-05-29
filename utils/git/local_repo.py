from __future__ import annotations

import os
import shutil
from tempfile import TemporaryDirectory

from git import Git
from git.repo import Repo as GitRepo
from git.exc import InvalidGitRepositoryError

from utils.git.file_changer import FileChanger

COMMITS_AHEAD_COUNT = 10
DIR_TO_BE_CHANGED = "b23df497a9"  # a random name


class LocalRepositoryException(Exception):
    pass


class LocalRepository:
    def __init__(self, location: str, origin_url: str):
        if not LocalRepository.exists(location, origin_url):
            LocalRepository.make_from_origin(location, origin_url)
        self.location = location
        self.origin_url = origin_url
        self._git = Git(location)
        self._git_git = Git(os.path.join(location, ".git"))

    @staticmethod
    def exists(location: str, origin_url: str):
        if not os.path.exists(location):
            print("not os.path.exists(location)")
            return False
        try:
            check_repo = GitRepo(location)
        except InvalidGitRepositoryError:
            print("InvalidGitRepositoryError")
            return False

        if check_repo.remote("origin").url != origin_url:
            print('check_repo.remote("origin").url != origin_url')
            print(check_repo.remote("origin").url, "!=", origin_url)
            return False

        dot_git_git_location = os.path.join(location, ".git", ".git")
        if not os.path.exists(dot_git_git_location):
            print("not os.path.exists(dot_git_git_location)")
            return False

        # also could've checked if it's `git pull`-able

        return True

    @staticmethod
    def make_from_origin(location: str, origin_url: str):
        if not os.path.exists(location):
            os.makedirs(location, exist_ok=True)
        if not os.path.isdir(location):
            raise LocalRepositoryException
        if len(os.listdir(location)) > 0:
            # not empty
            raise LocalRepositoryException(location)

        _git = Git(location)
        _git.clone(origin_url, ".")

        _git_git = Git(os.path.join(location, ".git"))
        _git_git.init()
        _git_git.add(".")
        _git_git.commit(message="git-git")

        with TemporaryDirectory() as temp_dir:
            os.rmdir(temp_dir)
            shutil.copytree(location, temp_dir)
            _git_to_push = Git(temp_dir)
            file_changer = FileChanger(
                os.path.join(temp_dir, DIR_TO_BE_CHANGED)
            )
            for i in range(COMMITS_AHEAD_COUNT):
                confirmation = (
                    "Yes, I know this action will irreversibly delete my files "
                    "on the path specified."
                )
                file_changer.change_files(confirmation)
                _git_to_push.add(".")
                _git_to_push.commit(message=f"load testing commit #{i}")
            _git_to_push.push()

        return LocalRepository(location, origin_url)

    def duplicate(self, dup_location):
        os.rmdir(dup_location)
        shutil.copytree(self.location, dup_location)
        return LocalRepository(dup_location, self.origin_url)

    def pull(self):
        self._git.pull()

    def revert_pull(self):
        self._git.reset(f"HEAD~{COMMITS_AHEAD_COUNT}", hard=True)
        self._git_git.clean("-df")
        self._git_git.restore(".")
