from __future__ import annotations

import dotenv
from pydantic import BaseSettings, Field

dotenv.load_dotenv()


class User(BaseSettings):
    username: str = Field(env="USERNAME")
    email: str = Field(env="EMAIL")
    password: str = Field(env="PASSWORD")


class Project(BaseSettings):
    name: str = Field(env="REPONAME")


class Urls:
    login: str = "/auth/login"
    main: str
    branches: str
    tags: str

    def __init__(self, config: WebsiteConfig) -> None:
        username = config.user.username
        project_name = config.project.name
        self.main = f"/project/{username}/{project_name}"
        self.branches = f"/project/{username}/{project_name}/branch"
        self.tags = f"/project/{username}/{project_name}/tag"


class WebsiteConfig(BaseSettings):
    user: User = User()
    project: Project = Project()
    urls: Urls | None

    def __init__(
        self,
        **args,
    ) -> None:
        super().__init__(
            **args,
        )
        self.urls = Urls(self)


config = WebsiteConfig()
