from functools import cached_property

import dotenv
from pydantic import BaseSettings, Field

dotenv.load_dotenv()


class User(BaseSettings):
    username: str = Field(env="USERNAME")
    email: str = Field(env="EMAIL")
    password: str = Field(env="PASSWORD")


class Project(BaseSettings):
    name: str = Field(env="REPONAME")


class Urls(BaseSettings):
    login: str = "/auth/login"
    _username: str = Field(env="USERNAME")
    _projectname: str = Field(env="REPONAME")

    @cached_property
    def main(self) -> str:
        return f"/project/{self._username}/{self._projectname}"

    @cached_property
    def branches(self) -> str:
        return f"/project/{self._username}/{self._projectname}/branch"

    @cached_property
    def tags(self) -> str:
        return f"/project/{self._username}/{self._projectname}/tag"


class WebsiteConfig(BaseSettings):
    user: User = User()
    project: Project = Project()
    urls: Urls = Urls()


config = WebsiteConfig()
