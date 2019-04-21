from apps.zucc.jwb.jwb_constant import JwbConstant
from apps.zucc.jwb.jwb_helper import JwbHelper
from apps.zucc.jwb.jwb_http import JwbHttp


class JwbSpider:
    @staticmethod
    def get_article_list(constant_id: int) -> [dict]:
        url = "http://zuccjwb.zucc.edu.cn/index.php"
        params = {
            'c': 'main',
            'a': 'tlist',
            'id': constant_id
        }
        res = JwbHttp().sess.get(url=url, params=params)
        res.encoding = 'gbk'
        return JwbHelper.parse_article_list(res.text)


if __name__ == '__main__':
    a = JwbSpider.get_article_list(JwbConstant.RCTZ)
    print(a)
