from bs4 import BeautifulSoup


class LoginPage:
    def __init__(self, html_str: str) -> None:
        _soup = BeautifulSoup(html_str, "html.parser")
        self._csrf = _soup.select_one("form.form-signin.user input[name=_csrf]")[
            "value"
        ]

    @property
    def csrf(self):
        return self._csrf
