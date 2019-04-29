from apps.zucc_jsxy.zucc_jsxy_constant import ZuccJsxyConstant
from apps.zucc_jsxy.zucc_jsxy_helper import ZuccJsxyHelper
from apps.zucc_jsxy.zucc_jsxy_http import ZuccJsxyHttp


class ZuccJsxySpider:
    @staticmethod
    def get_article_list(constant_id: int, start: int = 1, page_num: int = 15) -> [dict]:
        """
        获取文章列表
        :param constant_id: jsxy_constant定义的常量
        :param start: 开始页数
        :param page_num: 每页文件数量
        :return: 文章列表
        """
        url = "http://jsxy.zucc.edu.cn/module/web/jpage/dataproxy.jsp"
        params = {
            'startrecord': (start - 1) * page_num,
            'endrecord': start * page_num,
            'perpage': page_num
        }
        data = {
            'col': 1,
            'appid': 1,
            'webid': 2,
            'path': '/',
            'columnid': constant_id,
            'sourceContentType': 1,
            'unitid': 774,
            'webname': '',
            'permissiontype': 1,
        }
        res = ZuccJsxyHttp().sess.post(url, params=params, data=data)
        res_list = ZuccJsxyHelper.parse_article_list(res.text)
        return res_list


if __name__ == '__main__':
    jsxy = ZuccJsxySpider()
    a = jsxy.get_article_list(ZuccJsxyConstant.JXJW_JXTZ)
    print(a)
