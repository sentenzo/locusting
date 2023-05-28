from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class WebsiteConfig:
    user: User
    urls: Urls
    project: Project

    def __init__(self) -> None:
        self.user = User()
        self.urls = Urls()
        self.project = Project()


@dataclass
class User:
    username: str = os.getenv("USERNAME")
    email: str = os.getenv("EMAIL")
    password: str = os.getenv("PASSWORD")


@dataclass
class Project:
    name: str = os.getenv("REPONAME")


@dataclass
class Urls:
    main: str = f"/project/{User.username}/{Project.name}"
    branches: str = f"/project/{User.username}/{Project.name}/branch"
    tags: str = f"/project/{User.username}/{Project.name}/tag"


config = WebsiteConfig()
