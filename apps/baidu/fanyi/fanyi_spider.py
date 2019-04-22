from apps.baidu.fanyi.fanyi_helper import FanyiHelper
from apps.baidu.fanyi.fanyi_http import FanyiHttp


class FanyiSpider:
    @staticmethod
    def translate(keywords: str, from_: str = 'en', to: str = 'zh') -> str:
        """
        翻译
        :param keywords: 需要翻译的单词或句子
        :param from_: 从什么语言翻译
        :param to: 翻译到什么语言
        :return: 翻译的结果
        """
        url = "https://fanyi.baidu.com/basetrans"
        token = "98945f0628cf2a4b552845b3417270cd"
        data = {
            'query': keywords,
            'from': from_,
            'to': to,
            'token': token,
            'sign': FanyiHelper.get_sign(keywords)
        }
        res = FanyiHttp().post(url=url, data=data).json()
        return FanyiHelper.detail_translate_result(res)


if __name__ == '__main__':
    cls = FanyiSpider()
    r = cls.translate('你好', from_='zh', to='en')
    print(r)
