from libs.http import Http


class BiqubaoHttp(Http):
    def __init__(self):
        super().__init__(random_ua=True, proxy=True)
