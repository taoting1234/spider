import json
from requests.cookies import cookiejar_from_dict
from apps.bilibili.bilibili_helper import BilibiliHelper
from apps.bilibili.bilibili_http import BilibiliHttp
from libs.cookies import Cookies
from libs.geetest import Geetest
from libs.logger import logger


class BilibiliLoginSpider:
    def __init__(self, username: str, password: str, headless: bool = True):
        self.username = username
        self.password = password
        self.headless = headless
        self.sess = BilibiliHttp(login=True).sess
        self.csrf = None
        self.uid = None
        self.cookies = None

    def login(self):
        """
        登录总逻辑
        """
        try:
            self.load_from_disk()
            self.get_user_info()
        except:
            self.__login()
            self.save_to_disk()
            self.get_user_info()

    def __login(self, type_: int = 1):
        """
        登录bilibili
        :param type_: 登录方式 （1为selenium登录，2为api接口登录）
        """
        if type_ == 1:
            url = "https://passport.bilibili.com/login"
            geetest = Geetest(url, headless=self.headless)
            geetest.send_keys(self.username, '//*[@id="login-username"]')
            geetest.send_keys(self.password, '//*[@id="login-passwd"]')
            t = 0
            while 1:
                geetest.run()
                try:
                    geetest.url_to_be('https://www.bilibili.com/')
                    break
                except:
                    t += 1
                    if t >= 3:
                        raise Exception('极验验证失败')
            cookies = geetest.get_cookies()
            geetest.close()
        elif type_ == 2:
            url = "https://api.kaaass.net/biliapi/user/login?jsonerr=true"
            data = {
                'user': self.username,
                'passwd': self.password
            }
            res = BilibiliHttp(login=False).sess.post(url=url, data=data).json()
            if res.get('status') != 'OK':
                raise Exception('login failed', res['info'])
            cookies = res['cookies']
        else:
            raise Exception('type error')
        logger.info('login success')
        self.sess.cookies = cookiejar_from_dict(Cookies.list_to_dict(cookies))
        self.cookies = Cookies.list_to_str(cookies)
        self.csrf = BilibiliHelper.get_csrf(Cookies.list_to_dict(cookies))

    def save_to_disk(self):
        """
        保存cookies到本地
        """
        Cookies.save_to_disk(self.cookies, '{}.cookies'.format(self.username))

    def load_from_disk(self):
        """
        从本地获取cookies
        """
        cookies = Cookies.load_from_disk('{}.cookies'.format(self.username))
        self.cookies = cookies
        self.sess.cookies = cookiejar_from_dict(Cookies.str_to_dict(cookies))
        self.csrf = BilibiliHelper.get_csrf(Cookies.str_to_dict(cookies))

    def get_user_info(self):
        """
        获取用户信息
        """
        url = 'https://api.bilibili.com/x/web-interface/nav'
        res = self.sess.get(url).json()
        if res.get('code'):
            raise Exception('get user info failed')
        self.uid = str(res['data']['mid'])
        uname = res['data']['uname']
        logger.info('uid: %s', self.uid)
        logger.info('uname: %s', uname)

    def follow_user(self, uid: int):
        """
        关注用户
        :param uid: 用户的uid
        """
        url = "https://api.bilibili.com/x/relation/modify"
        data = {
            'fid': uid,
            'act': 1,
            're_src': 11,
            'csrf': self.csrf
        }
        res = self.sess.post(url=url, data=data).json()
        if res.get('code'):
            raise Exception('follow user failed', res.get('message'))
        logger.info('follow user success: %s', uid)

    def unfollow_user(self, uid: int):
        """
        取消关注用户
        :param uid: 用户的uid
        """
        url = "https://api.bilibili.com/x/relation/modify"
        data = {
            'fid': uid,
            'act': 2,
            're_src': 11,
            'csrf': self.csrf
        }
        res = self.sess.post(url=url, data=data).json()
        if res.get('code'):
            raise Exception('unfollow user failed', res.get('message'))
        logger.info('unfollow user success: %s', uid)

    def create_dynamic(self, content: str):
        """
        创建动态
        :param content: 动态内容
        """
        url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/create"
        data = {
            'dynamic_id': 0,
            'type': 4,
            'rid': 0,
            'content': content,
            'extension': '{"emoji_type": 1}',
            'at_uids': '',
            'ctrl': '[]',
            'csrf_token': self.csrf
        }
        res = self.sess.post(url=url, data=data).json()
        if res.get('code'):
            raise Exception('create dynamic failed', res.get('msg'))
        dynamic_id = res['data']['dynamic_id']
        logger.info('create dynamic success: %s', dynamic_id)

    def remove_dynamic(self, dynamic_id: int):
        """
        删除动态
        :param dynamic_id: 动态id
        """
        url = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/rm_rp_dyn"
        data = {
            'uid': self.uid,
            'dynamic_id': dynamic_id,
            'csrf_token': self.csrf,
        }
        res = self.sess.post(url=url, data=data).json()
        if res.get('code'):
            raise Exception('remove dynamic failed', res.get('msg'))
        logger.info('remove dynamic success: %s %s', dynamic_id, res['data']['errmsg'])

    def repost_dynamic(self, dynamic_id: int, content: str, at_uids: [int]):
        """
        转发动态
        :param dynamic_id: 要转发的动态id
        :param content: 动态内容
        :param at_uids: at用户的列表
        """
        url = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost"
        data = {
            'uid': self.uid,
            'dynamic_id': dynamic_id,
            'content': '',
            'at_uids': '',
            'extension': '{"emoji_type": 1}',
            'ctrl': '[',
            'csrf_token': self.csrf
        }
        ctrl_data = []
        location = 0
        for uid in at_uids:
            name = BiliBiliNoLoginSpider.get_username_by_uid(uid)
            data['content'] += '@{} '.format(name)
            data['at_uids'] += '{},'.format(uid)
            ctrl_data.append({
                "data": str(uid),
                "location": location,
                "length": len(name) + 1,
                "type": 1
            })
            location += len(name) + 2
        data['content'] += content
        data['at_uids'] = data['at_uids'][:-1]
        data['ctrl'] = json.dumps(ctrl_data)
        res = self.sess.post(url=url, data=data).json()
        if res.get('code'):
            raise Exception('post dynamic failed', res.get('msg'))
        logger.info('post dynamic success: %s', res['data']['errmsg'])

    def get_dynamic_list(self):
        """
        获取动态列表
        :return: 动态列表
        """
        url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new"
        params = {
            'uid': self.uid,
            'type': '268435455'  # 不知道啥意思
        }
        res = self.sess.get(url, params=params).json()
        if res.get('code'):
            raise Exception('get dynamic list failed', res.get('msg'))
        res_list = BilibiliHelper.parse_dynamic_list(res)
        logger.info('get dynamic list success: %s', res_list)
        return res_list


class BiliBiliNoLoginSpider:
    @staticmethod
    def get_username_by_uid(uid: int):
        """
        通过uid获取用户名
        :param uid: 用户uid
        :return: 用户的用户名
        """
        url = "https://api.bilibili.com/x/space/acc/info"
        params = {
            'mid': uid
        }
        res = BilibiliHttp(False).sess.get(url=url, params=params).json()
        if res.get('code'):
            raise Exception('get username failed', res.get('msg'))
        name = res['data']['name']
        logger.info('get username success: %s', name)
        return name

    @staticmethod
    def get_dynamic_list_by_uid(uid: int):
        """
        通过uid获取动态列表
        :param uid: 用户uid
        :return: 动态列表
        """
        url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"
        params = {
            'host_uid': uid
        }
        res = BilibiliHttp(False).sess.get(url=url, params=params).json()
        if res.get('code'):
            raise Exception('get dynamic list failed', res.get('msg'))
        res_list = BilibiliHelper.parse_dynamic_list(res)
        logger.info('get dynamic list success: %s', res_list)
        return res_list

    @staticmethod
    def get_lottery_notice(dynamic_id: int):
        """
        获取抽奖信息
        :param dynamic_id: 动态id
        :return: 抽奖信息
        """
        url = "https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice"
        params = {
            'dynamic_id': dynamic_id
        }
        res = BilibiliHttp(False).sess.get(url=url, params=params).json()
        if res.get('code'):
            raise Exception('get lottery notice failed', res.get('msg'))
        data = BilibiliHelper.parse_lottery_notice(res)
        logger.info('get lottery notice success: %s', data)
        return data

    @staticmethod
    def get_followings_by_uid(uid: int, pn: int = 1, ps: int = 20, order: str = 'desc'):
        """
        通过uid获取关注列表
        :param uid: 用户uid
        :param pn: 第几页
        :param ps: 每页个数
        :param order: 排序规则
        :return: 关注列表
        """
        url = "https://api.bilibili.com/x/relation/followings"
        params = {
            'vmid': uid,
            'pn': pn,
            'ps': ps,
            'order': order
        }
        res = BilibiliHttp(False).sess.get(url, params=params).json()
        res_list = BilibiliHelper.parse_followings_list(res)
        return res_list

    @staticmethod
    def get_follow_stat_by_uid(uid: int):
        """
        通过uid获取关注人数和粉丝人数
        :param uid: 用户uid
        :return: 关注人数和粉丝人数
        """
        url = "https://api.bilibili.com/x/relation/stat"
        params = {
            'vmid': uid
        }
        res = BilibiliHttp(False).sess.get(url, params=params).json()
        if res.get('code'):
            raise Exception('get follow stat failed %s', res.get('message'))
        data = {
            'following': res['data']['following'],
            'follower': res['data']['follower']
        }
        logger.info('get follow stat success %s', data)
        return data


if __name__ == '__main__':
    user = BilibiliLoginSpider('username', 'password', False)
    user.login()

    a = BiliBiliNoLoginSpider.get_followings_by_uid(111111)
    print(a)
