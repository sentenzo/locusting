from __future__ import annotations

import os


class WebsiteConfig:
    user: User
    urls: Urls
    project: Project

    def __init__(self) -> None:
        self.user = User()
        self.urls = Urls()
        self.project = Project()


class User:
    username: str = os.getenv("USERNAME")
    email: str = os.getenv("EMAIL")
    password: str = os.getenv("PASSWORD")


class Project:
    name: str = os.getenv("REPONAME")


class Urls:
    main: str = f"/project/{User.username}/{Project.name}"
    branches: str = f"/project/{User.username}/{Project.name}/branch"
    tags: str = f"/project/{User.username}/{Project.name}/tag"


config = WebsiteConfig()
