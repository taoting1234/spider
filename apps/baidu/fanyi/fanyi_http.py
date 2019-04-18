from libs.http import Http


class FanyiHttp(Http):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sess.headers['Referer'] = "https://fanyi.baidu.com/"
        self.sess.headers['Host'] = "fanyi.baidu.com"
        self.sess.headers['Cookie'] = \
            "BAIDUID=4EF42ED6D3A40D295D50EF4322040ED3:FG=1; BIDUPSID=4EF42ED6D3A40D295D50EF4322040ED3; PSTM=1551257824; MCITY=-179%3A; cflag=13%3A3; locale=zh; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; pgv_pvi=701502464; H_PS_PSSID=1425_21086_20698_28775_28724_28557_28839_28585_28604; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1555468706,1555504275,1555566101; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1555504275,1555565956,1555566095,1555566101; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1555569445; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1555569445"
