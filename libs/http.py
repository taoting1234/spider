import requests
from faker import Faker
from config import *

from libs.proxy import Proxy


class Http:
    def __init__(self, random_ua=False, proxy=False):
        self.sess = requests.session()
        if random_ua:
            self.sess.headers['User-Agent'] = Faker().user_agent()
        else:
            self.sess.headers['User-Agent'] = default_ua
        if proxy:
            self.sess.proxies = Proxy.get_proxy()
