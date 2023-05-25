import os
import time

from locust.clients import HttpSession

from utils.parser import LoginPage


def web_shot(http_client: HttpSession):
    login_csrf = None
    with http_client.get("/auth/login") as response:
        login_csrf = LoginPage(response.text).csrf
    form_data = {
        "_csrf": login_csrf,
        "email": os.getenv("EMAIL"),
        "password": os.getenv("PASSWORD"),
        "rememberMe": "",
    }
    print(form_data)
    http_client.post(
        "/auth/login",
        data=form_data,
    )
    username = os.getenv("USERNAME")
    reponame = os.getenv("REPONAME")
    time.sleep(1)
    http_client.get(f"/project/{username}/{reponame}")
    time.sleep(1)
    http_client.get(f"/project/{username}/{reponame}/branch")
    time.sleep(1)
    http_client.get(f"/project/{username}/{reponame}/tag")
    time.sleep(1)

    http_client.cookies.clear()
