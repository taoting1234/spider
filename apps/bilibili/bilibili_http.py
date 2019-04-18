from libs.http import Http


class BilibiliHttp(Http):
    def __init__(self, login: bool):
        if login:
            super().__init__(random_ua=False, proxy=False)
        else:
            super().__init__(random_ua=True, proxy=True)
