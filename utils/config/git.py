from __future__ import annotations

import os


class GitConfig:
    git_user: GitUser
    remote_repo: RemoteRepository
    local_repo: LocalRepository

    def __init__(self) -> None:
        self.git_user = GitUser()
        self.remote_repo = RemoteRepository()
        self.local_repo = LocalRepository()


class GitUser:
    pass


class RemoteRepository:
    clone_url: str = os.getenv("REOPURL")


class LocalRepository:
    location: str = "./local_repo"


config = GitConfig()
