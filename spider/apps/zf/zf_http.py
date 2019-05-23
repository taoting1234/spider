from urllib.parse import urlencode
from requests import Response

from spider.libs.http import Http


class ZfHttp(Http):
    encoding = 'gbk'

    def __init__(self):
        super().__init__()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.headers.update(headers)

    def _before_request(self, url: str, params: dict, data: dict) -> (str, str):
        if params:
            url += "?" + urlencode(params, encoding=self.encoding)
        if data:
            data = urlencode(data, encoding=self.encoding)
        return url, data

    def _end_request(self, res: Response) -> Response:
        res.encoding = self.encoding
        return res
