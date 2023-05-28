import dotenv

from .git import config as git_config
from .website import config as website_config

dotenv.load_dotenv()


__all__ = ["website_config", "git_config"]
