import dotenv

from .website import config as website_config

dotenv.load_dotenv()


__all__ = ["website_config"]
