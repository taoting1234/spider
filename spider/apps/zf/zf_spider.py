from io import BytesIO

from requests import Response

from spider.apps.zf.zf_helper import ZfHelper
from spider.apps.zf.zf_http import ZfHttp
from spider.libs.logger import logger


class ZfSpider:
    def __init__(self, id_: str, password: str, xn: str = '2018-2019', xq: str = '1',
                 host: str = 'xk.zucc.edu.cn'):
        """
        :param _id: 学号
        :param password: 密码
        :param xn: 学年
        :param xq: 学期
        :param host: 网站域名
        """
        self.id = id_
        self.password = password
        self.xn = xn
        self.xq = xq
        self.host = host
        self.sess = ZfHttp()
        self.is_login = False
        self.username = None
        self.main_url = None

    def __get_index(self) -> Response:
        """
        获取首页
        :return: 首页response对象
        """
        url = 'http://{}/'.format(self.host)
        res = self.sess.get(url=url)
        return res

    def __get_checkcode(self) -> str:
        """
        获取验证码
        :return: 验证码的文本
        """
        index_res = self.__get_index()
        url = 'http://{}/CheckCode.aspx'.format(self.host)
        self.sess.headers.update({'Referer': index_res.url})
        res = self.sess.get(url=url)
        image = BytesIO(res.content)
        return ZfHelper.get_checkcode(image)

    def login(self):
        """
        登录
        """
        index_res = self.__get_index()
        code = self.__get_checkcode()
        url = index_res.url
        data = {
            '__VIEWSTATE': ZfHelper.get_viewstate(index_res.text),
            'txtUserName': self.id,
            'Textbox1': '',
            'TextBox2': self.password,
            'txtSecretCode': code,
            'RadioButtonList1': '学生',
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': '',
        }
        self.sess.headers.update({'Referer': url})
        res = self.sess.post(url=url, data=data)
        if res.url == index_res.url:
            info = ZfHelper.get_alert_info(res.text)
            # 判断失败原因
            if '验证码' in info:
                logger.debug('验证码错误，正在重试')
                return self.login()
            raise Exception(('登录失败:%s', info))
        # 获取信息
        self.username = ZfHelper.get_username(res.text)
        self.is_login = True
        self.main_url = res.url

    def __get_class_schedule(self):
        url = 'http://' + self.host + '/xskbcx.aspx'
        params = {
            'xh': self.id,
            'xm': self.username,
            'gnmkdm': 'N121603'
        }
        self.sess.headers.update({'Referer': self.main_url})
        res = self.sess.get(url=url, params=params)
        xn = ZfHelper.get_current_xn(res.text)
        xq = ZfHelper.get_current_xq(res.text)
        if xn == self.xn and xq == self.xq:
            return res

        data = {
            '__EVENTTARGET': 'xnd',
            '__VIEWSTATE': ZfHelper.get_viewstate(res.text),
            'xnd': self.xn,
            'xqd': xq
        }
        res = self.sess.post(url=url, params=params, data=data)
        xn = ZfHelper.get_current_xn(res.text)
        xq = ZfHelper.get_current_xq(res.text)
        if xn == self.xn and xq == self.xq:
            return res

        data = {
            '__EVENTTARGET': 'xqd',
            '__VIEWSTATE': ZfHelper.get_viewstate(res.text),
            'xnd': self.xn,
            'xqd': self.xq
        }
        res = self.sess.post(url=url, params=params, data=data)
        return res

    def get_class_schedule(self) -> [dict]:
        """
        获取课程表
        """
        if self.is_login is False:
            self.login()
        res = self.__get_class_schedule()
        xn = ZfHelper.get_current_xn(res.text)
        xq = ZfHelper.get_current_xq(res.text)
        assert xn == self.xn
        assert xq == self.xq
        return res

    def __get_grade(self):
        url = 'http://{}/xscj_gc2.aspx'.format(self.host)
        params = {
            'xh': self.id,
            'xm': self.username,
            'gnmkdm': 'N121617'
        }
        self.sess.headers.update({'Referer': self.main_url})
        res = self.sess.get(url=url, params=params)

        data = {
            '__VIEWSTATE': ZfHelper.get_viewstate(res.text),
            'ddlXN': self.xn,
            'ddlXQ': self.xq,
            'Button1': '按学期查询'
        }
        res = self.sess.post(url=url, params=params, data=data)
        return res

    def get_grade(self) -> [dict]:
        """
        获取成绩
        """
        if self.is_login is False:
            self.login()
        res = self.__get_grade()
        return ZfHelper.detail_grade(res.text)

    def __get_examination_room(self):
        url = 'http://' + self.host + '/xskscx.aspx'
        params = {
            'xh': self.id,
            'xm': self.username,
            'gnmkdm': 'N121604'
        }
        self.sess.headers.update({'Referer': self.main_url})
        res = self.sess.get(url=url, params=params)
        xn = ZfHelper.get_current_xn(res.text)
        xq = ZfHelper.get_current_xq(res.text)
        if xn == self.xn and xq == self.xq:
            return res

        data = {
            '__EVENTTARGET': 'xnd',
            '__VIEWSTATE': ZfHelper.get_viewstate(res.text),
            'xnd': self.xn,
            'xqd': xq
        }
        res = self.sess.post(url=url, params=params, data=data)
        xn = ZfHelper.get_current_xn(res.text)
        xq = ZfHelper.get_current_xq(res.text)
        if xn == self.xn and xq == self.xq:
            return res

        data = {
            '__EVENTTARGET': 'xqd',
            '__VIEWSTATE': ZfHelper.get_viewstate(res.text),
            'xnd': self.xn,
            'xqd': self.xq
        }
        res = self.sess.post(url=url, params=params, data=data)
        return res

    def get_examination_room(self) -> [dict]:
        """
        获取考场
        """
        if self.is_login is False:
            self.login()
        res = self.__get_examination_room()
        xn = ZfHelper.get_current_xn(res.text)
        xq = ZfHelper.get_current_xq(res.text)
        assert xn == self.xn
        assert xq == self.xq
        return ZfHelper.detail_examination_room(res.text)

    def __get_makeup_examination_room(self):
        url = 'http://' + self.host + '/XsBkKsCx.aspx'
        params = {
            'xh': self.id,
            'xm': self.username,
            'gnmkdm': 'N121608'
        }
        self.sess.headers.update({'Referer', self.main_url})
        res = self.sess.get(url=url, params=params)
        xn = ZfHelper.get_current_xn(res.text)
        xq = ZfHelper.get_current_xq(res.text)
        if xn == self.xn and xq == self.xq:
            return res

        data = {
            '__EVENTTARGET': 'xnd',
            '__VIEWSTATE': ZfHelper.get_viewstate(res.text),
            'xnd': self.xn,
            'xqd': xq
        }
        res = self.sess.post(url=url, params=params, data=data)
        xn = ZfHelper.get_current_xn(res.text)
        xq = ZfHelper.get_current_xq(res.text)
        if xn == self.xn and xq == self.xq:
            return res

        data = {
            '__EVENTTARGET': 'xqd',
            '__VIEWSTATE': ZfHelper.get_viewstate(res.text),
            'xnd': self.xn,
            'xqd': self.xq
        }
        res = self.sess.post(url=url, params=params, data=data)
        return res

    def get_makeup_examination_room(self) -> [dict]:
        """
        获取补考考场
        """
        if self.is_login is False:
            self.login()
        res = self.__get_makeup_examination_room()
        xn = ZfHelper.get_current_xn(res.text)
        xq = ZfHelper.get_current_xq(res.text)
        assert xn == self.xn
        assert xq == self.xq
        r = ZfHelper.detail_makeup_examination_room(res.text)
        return r


if __name__ == '__main__':
    user = ZfSpider('username', 'password', '2018-2019', '1')
    user.login()
    rr = user.get_grade()
    print(rr)
