from requests import Response

from libs.http import Http


class BiqubaoHttp(Http):
    encoding = 'gbk'

    def __init__(self):
        super().__init__(random_ua=True, proxy=True)

    def _end_request(self, res: Response) -> Response:
        res.encoding = self.encoding
        return res
