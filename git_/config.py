import dotenv
from pydantic import BaseSettings, Field

dotenv.load_dotenv()


class GitUser(BaseSettings):
    pass


class RemoteRepository(BaseSettings):
    clone_url: str = Field(env="REPOURL")


class LocalRepository(BaseSettings):
    location: str = Field(env="LOCAL_REPO_PATH")


class GitConfig(BaseSettings):
    git_user: GitUser = GitUser()
    remote_repo: RemoteRepository = RemoteRepository()
    local_repo: LocalRepository = LocalRepository()


config = GitConfig()
