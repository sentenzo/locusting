from bs4 import BeautifulSoup


def parse_login_csrf(html_str: str) -> str:
    soup = BeautifulSoup(html_str, "html.parser")
    _csrf = soup.select_one("form.form-signin.user input[name=_csrf]")["value"]
    return _csrf
