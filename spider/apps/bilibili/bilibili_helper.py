import json


class BilibiliHelper:
    @staticmethod
    def get_csrf(cookies: dict) -> str:
        for i, j in cookies.items():
            if i == 'bili_jct':
                return j
        raise Exception('get csrf failed')

    @staticmethod
    def parse_dynamic_list(raw: dict) -> list:
        res = []
        for i in raw['data'].get('cards', []):
            try:
                card = json.loads(i['card'])
                data = {
                    'dynamic_id': i['desc']['dynamic_id'],
                    'uid': card['user']['uid'],
                    'is_lott': True if i.get('extension', {}).get('lott') else False
                }
                res.append(data)
                if i['desc']['orig_dy_id']:
                    data = {
                        'dynamic_id': i['desc']['orig_dy_id'],
                        'uid': card['origin_user']['info']['uid'],
                        'is_lott': True if card.get('origin_extension', {}).get('lott') else False
                    }
                    res.append(data)
            except:
                pass
        return res

    @staticmethod
    def parse_lottery_notice(raw: dict) -> dict:
        msg = "一等奖:{} {}人".format(raw['data']['first_prize_cmt'], raw['data']['first_prize'])
        if raw['data']['second_prize']:
            msg += " 二等奖:{} {}人".format(raw['data']['second_prize_cmt'], raw['data']['second_prize'])
        if raw['data']['third_prize']:
            msg += " 三等奖:{} {}人".format(raw['data']['third_prize_cmt'], raw['data']['third_prize'])

        data = {
            'msg': msg,
            'need_post': bool(raw['data']['need_post']),
            'lottery_at_num': raw['data']['lottery_at_num'],
            'lottery_time': raw['data']['lottery_time']
        }
        return data

    @staticmethod
    def parse_followings_list(raw: dict) -> list:
        return [i['mid'] for i in raw['data']['list']]
