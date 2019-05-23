import re
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image


class ZfHelper:
    @staticmethod
    def get_checkcode(image: BytesIO) -> str:
        try:
            file = {'file': image}
            res = requests.post(url="http://zf-server.newitd.com/upload", files=file, timeout=5)
            res.raise_for_status()
            return res.text
        except:
            img = Image.open(image)
            img.show()
            return input("请输入验证码：")

    @staticmethod
    def get_viewstate(raw: str) -> str:
        try:
            viewstate = re.search('<input type="hidden" name="__VIEWSTATE" value="(.*)" />', raw).group(1)
            return viewstate
        except:
            return ""

    @staticmethod
    def get_alert_info(raw: str):
        try:
            return re.search("alert\\('(.*)'\\);", raw).group(1)
        except Exception as e:
            raise Exception("解析返回信息失败", e)

    @staticmethod
    def get_username(raw: str) -> str:
        try:
            return re.search('<span id="xhxm">(.*)同学</span>', raw).group(1)
        except Exception as e:
            raise Exception("解析姓名信息失败", e)

    @staticmethod
    def get_student_info(raw):
        try:
            soup = BeautifulSoup(raw, "lxml")
            a = soup.select("#Label3")[0].text
            r = re.search("^学号:(.*) {2}姓名:(.*) {2}学院:(.*) {2}行政班:(.*)$", a)
            rr = re.search(
                '<span id="xsxxmc">专业名称：</span><input name="zymc" type="text" value="(.*)" readonly="readonly"',
                raw)
            grade = re.search('<option selected="selected" value="(.*)">(.*)</option>', raw).group(1)
            d = {
                'college': r.group(3),
                'administrative_class': r.group(4),
                'professional_title': rr.group(1),
                'grade': grade
            }
            return d
        except Exception as e:
            raise Exception("获取基本信息失败", e)

    @staticmethod
    def get_current_xn(raw: str) -> str:
        soup = BeautifulSoup(raw, "lxml")
        a = soup.select("#xnd > option")
        for i in a:
            if i.get('selected'):
                return i.text

    @staticmethod
    def get_current_xq(raw: str) -> str:
        soup = BeautifulSoup(raw, "lxml")
        a = soup.select("#xqd > option")
        for i in a:
            if i.get('selected'):
                return i.text

    @staticmethod
    def detail_grade(raw: str) -> [dict]:
        try:
            soup = BeautifulSoup(raw, "lxml")
            a = soup.select(".datelist > tr")
            a.pop(0)
            b = [i.contents for i in a]
            c = []
            for i in b:
                if i[1].text == '课程性质名称':
                    break
                c.append({
                    '课程名称': ''.join(i[4].text.split()),
                    '学分': ''.join(i[7].text.split()),
                    '绩点': ''.join(i[8].text.split()),
                    '成绩': ''.join(i[9].text.split())
                })
            return c
        except Exception as e:
            raise Exception('解析成绩详细信息失败', e)

    @staticmethod
    def detail_examination_room(raw: str) -> [dict]:
        try:
            soup = BeautifulSoup(raw, "lxml")
            a = soup.select(".datelist > tr")
            a.pop(0)
            b = [i.contents for i in a]
            c = []
            for i in b:
                c.append({
                    '课程名称': ''.join(i[2].text.split()),
                    '时间': ''.join(i[4].text.split()),
                    '教室': ''.join(i[5].text.split()),
                    '座位号': ''.join(i[7].text.split())
                })
            return c
        except Exception as e:
            raise Exception('解析考场失败', e)

    @staticmethod
    def detail_makeup_examination_room(raw: str) -> [dict]:
        try:
            soup = BeautifulSoup(raw, "lxml")
            a = soup.select(".datelist > tr")
            a.pop(0)
            b = [i.contents for i in a]
            c = []
            for i in b:
                c.append({
                    '课程名称': ''.join(i[2].text.split()),
                    '时间': ''.join(i[4].text.split()),
                    '教室': ''.join(i[5].text.split()),
                    '座位号': ''.join(i[6].text.split())
                })
            return c
        except Exception as e:
            raise Exception('解析补考考场失败', e)
