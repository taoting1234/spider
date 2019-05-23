import requests
from spider.config import *


class Proxy:
    @staticmethod
    def get_proxy():
        url = proxy_url
        res = requests.get(url).json()
        return res['msg']

    def get_proxy_dict(self):
        proxy = self.get_proxy()
        return {
            "http": proxy,
            "https": proxy
        }


if __name__ == '__main__':
    a = Proxy.get_proxy()
    print(a)
