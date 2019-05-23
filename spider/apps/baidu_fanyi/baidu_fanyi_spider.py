from spider.apps.baidu_fanyi.baidu_fanyi_helper import BaiduFanyiHelper
from spider.apps.baidu_fanyi.baidu_fanyi_http import BaiduFanyiHttp


class BaiduFanyiSpider:
    token = "98945f0628cf2a4b552845b3417270cd"

    @classmethod
    def base_translate(cls, data: str, from_: str = 'en', to: str = 'zh') -> str:
        """
        基础翻译
        :param data: 需要翻译的单词或句子
        :param from_: 从什么语言翻译
        :param to: 翻译到什么语言
        :return: 翻译的结果
        """
        url = "https://fanyi.baidu.com/basetrans"
        data = {
            'query': data,
            'from': from_,
            'to': to,
            'token': cls.token,
            'sign': BaiduFanyiHelper.get_sign(data)
        }
        res = BaiduFanyiHttp().post(url=url, data=data).json()
        return BaiduFanyiHelper.detail_base_translate_result(res)

    @classmethod
    def paragraph_translate(cls, data: str, from_: str = 'en', to: str = 'zh') -> list:
        """
        段落翻译
        :param data: 需要翻译的文章
        :param from_: 从什么语言翻译
        :param to: 翻译到什么语言
        :return: 翻译的结果
        """
        url = "https://fanyi.baidu.com/v2transapi"
        data = {
            'query': data,
            'from': from_,
            'to': to,
            'token': cls.token,
            'sign': BaiduFanyiHelper.get_sign(data),
            'transtype': 'translang',
            'simple_means_flag': 3
        }
        res = BaiduFanyiHttp().post(url=url, data=data).json()
        return BaiduFanyiHelper.detail_paragraph_translate_result(res)


if __name__ == '__main__':
    cls = BaiduFanyiSpider()
    s = """
    PySnooper is a poor man's debugger.

You're trying to figure out why your Python code isn't doing what you think it should be doing. You'd love to use a full-fledged debugger with breakpoints and watches, but you can't be bothered to set one up right now.

You want to know which lines are running and which aren't, and what the values of the local variables are.

Most people would use print lines, in strategic locations, some of them showing the values of variables.

PySnooper lets you do the same, except instead of carefully crafting the right print lines, you just add one decorator line to the function you're interested in. You'll get a play-by-play log of your function, including which lines ran and when, and exactly when local variables were changed.

What makes PySnooper stand out from all other code intelligence tools? You can use it in your shitty, sprawling enterprise codebase without having to do any setup. Just slap the decorator on, as shown below, and redirect the output to a dedicated log file by specifying its path as the first argument.

"""
    r = cls.paragraph_translate(s, from_='en', to='zh')
    print(r)
