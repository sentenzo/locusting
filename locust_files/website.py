import os
import time
import dotenv
from locust import HttpUser, between, task, run_single_user


from locust.clients import HttpSession

from utils.web.parser import parse_login_csrf

dotenv.load_dotenv()

username = os.getenv("USERNAME")
reponame = os.getenv("REPONAME")
url_proj_main = f"/project/{username}/{reponame}"
url_proj_branches = f"/project/{username}/{reponame}/branch"
url_proj_tags = f"/project/{username}/{reponame}/tag"


class WebUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        with self.client.get("/auth/login") as response:
            login_csrf = parse_login_csrf(response.text)
        form_data = {
            "_csrf": login_csrf,
            "email": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD"),
            "rememberMe": "",
        }
        self.client.post(
            "/auth/login",
            data=form_data,
        )

    def on_stop(self):
        self.client.cookies.clear()

    @task(10)
    def get_proj_main(self):
        self.client.get(url_proj_main)

    @task(10)
    def get_proj_branches(self):
        self.client.get(url_proj_branches)

    @task(10)
    def get_proj_tags(self):
        self.client.get(url_proj_tags)

    @task(1)
    def relogin(self):
        self.on_stop()
        self.on_start()


if __name__ == "__main__":
    run_single_user(WebUser)
