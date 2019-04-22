from faker import Faker
from requests import Response
from config import *
from libs.proxy import Proxy
import requests


class Http:
    def __init__(self, random_ua=False, proxy=False):
        self.sess = requests.session()
        if random_ua:
            self.sess.headers['User-Agent'] = Faker().user_agent()
        else:
            self.sess.headers['User-Agent'] = default_ua
        if proxy:
            self.sess.proxies = Proxy.get_proxy()

    @property
    def headers(self):
        return self.sess.headers

    def get(self, **kwargs):
        return self._request('GET', **kwargs)

    def post(self, **kwargs):
        return self._request('POST', **kwargs)

    def _request(self, method: str, url: str, params: dict = None, data: dict = None,
                 encoding: str = None) -> Response:
        """
        http请求
        :param method: 请求方法
        :param url: url
        :param params: 请求参数
        :param data: 请求数据
        :param encoding: 编码
        :return: request之后的Response对象
        """
        url, data = self._before_request(url, params, data)
        res = self.sess.request(method, url=url, data=data)
        res = self._end_request(res)
        return res

    @staticmethod
    def _before_request(url: str, params: dict, data: dict) -> (str, str):
        """
        request之前的准备，可根据逻辑重载
        :param url: url
        :param params: 请求参数
        :param data: 请求
        :return: url，data元组
        """
        # 逻辑写这里
        pass
        return url, data

    @staticmethod
    def _end_request(res: Response) -> Response:
        """
        request之后的处理，可根据逻辑重载
        :param res: request之后的Response对象
        :return: 处理之后的Response对象
        """
        # 逻辑写这里
        pass
        return res
