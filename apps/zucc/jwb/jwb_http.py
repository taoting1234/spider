from requests import Response

from libs.http import Http


class JwbHttp(Http):
    encoding = 'gbk'

    def __init__(self):
        super().__init__()

    def _end_request(self, res: Response) -> Response:
        res.encoding = self.encoding
        return res
