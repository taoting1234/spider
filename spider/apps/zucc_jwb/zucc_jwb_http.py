from requests import Response

from spider.libs.http import Http


class ZuccJwbHttp(Http):
    encoding = 'gbk'

    def __init__(self):
        super().__init__()

    def _end_request(self, res: Response) -> Response:
        res.encoding = self.encoding
        return res
