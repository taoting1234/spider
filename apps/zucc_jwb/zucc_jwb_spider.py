from apps.zucc_jwb.zucc_jwb_constant import ZuccJwbConstant
from apps.zucc_jwb.zucc_jwb_helper import ZuccJwbHelper
from apps.zucc_jwb.zucc_jwb_http import ZuccJwbHttp


class ZuccJwbSpider:
    @staticmethod
    def get_article_list(constant_id: int) -> [dict]:
        url = "http://zuccjwb.zucc.edu.cn/index.php"
        params = {
            'c': 'main',
            'a': 'tlist',
            'id': constant_id
        }
        res = ZuccJwbHttp().get(url=url, params=params)
        return ZuccJwbHelper.parse_article_list(res.text)


if __name__ == '__main__':
    a = ZuccJwbSpider.get_article_list(ZuccJwbConstant.RCTZ)
    print(a)
