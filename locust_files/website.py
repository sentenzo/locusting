from locust import HttpUser, between, run_single_user, task

from web.config import config
from web.parser import parse_login_csrf


class WebUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        with self.client.get(config.urls.login) as response:
            login_csrf = parse_login_csrf(response.text)
        form_data = {
            "_csrf": login_csrf,
            "email": config.user.email,
            "password": config.user.password,
            "rememberMe": "",
        }
        self.client.post(
            config.urls.login,
            data=form_data,
        )

    def on_stop(self):
        self.client.cookies.clear()

    @task(100)
    def get_proj_main(self):
        self.client.get(config.urls.main)

    @task(100)
    def get_proj_branches(self):
        self.client.get(config.urls.branches)

    @task(100)
    def get_proj_tags(self):
        self.client.get(config.urls.tags)

    @task(1)
    def relogin(self):
        self.on_stop()
        self.on_start()


if __name__ == "__main__":
    run_single_user(WebUser)
