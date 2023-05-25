import dotenv
from locust import HttpUser, between, task

from utils.web_shoot import web_shot

dotenv.load_dotenv()


class Locuster(HttpUser):
    wait_time = between(1, 5)

    @task
    def user_lands_by_web(self):
        web_shot(self.client)

    @task
    def git_pull(self):
        ...
