from apps.baidu.fanyi.fanyi_helper import FanyiHelper
from apps.baidu.fanyi.fanyi_http import FanyiHttp


class FanyiSpider:
    def __init__(self, *args, **kwargs):
        self.sess = FanyiHttp(*args, **kwargs).sess

    def translate(self, keywords: str, from_: str = 'en', to: str = 'zh') -> str:
        url = "https://fanyi.baidu.com/basetrans"
        token = "98945f0628cf2a4b552845b3417270cd"
        data = {
            'query': keywords,
            'from': from_,
            'to': to,
            'token': token,
            'sign': FanyiHelper.get_sign(keywords)
        }
        res = self.sess.post(url=url, data=data).json()
        return FanyiHelper.detail_translate_result(res)


if __name__ == '__main__':
    cls = FanyiSpider()
    r = cls.translate('hello world')
    print(r)
