import random
import re
import requests
import time
import platform
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from io import BytesIO
from libs.cookies import Cookies
from libs.logger import logger


class Geetest:
    def __init__(self, url: str,
                 bg_image_class: str = 'gt_cut_bg_slice',
                 fullbg_image_class: str = 'gt_cut_fullbg_slice',
                 button_xpath: str = '//*[@id="gc-box"]/div/div[3]/div[2]',
                 headless: bool = False,
                 timeout: int = 10):
        self.timeout: int = timeout
        self.url: str = url
        self.bg_image_class = bg_image_class
        self.fullbg_image_class = fullbg_image_class
        self.button_xpath = button_xpath
        self.driver: webdriver = self.create_driver(headless)
        self.WAIT: WebDriverWait = WebDriverWait(self.driver, self.timeout)

    def run(self):
        bg_image_file, bg_location_list = self.get_images(self.bg_image_class)
        fullbg_image_file, fullbg_location_list = self.get_images(self.fullbg_image_class)
        bg_image = self.merge_image(bg_image_file, bg_location_list)
        fullbg_image = self.merge_image(fullbg_image_file, fullbg_location_list)
        distance = self.get_distance(bg_image, fullbg_image)
        track = self.get_track(distance)
        self.drag_the_ball(track)

    def create_driver(self, headless: bool):
        options = webdriver.ChromeOptions()
        options.add_argument("log-level=3")
        if headless:
            options.add_argument("headless")
        else:
            options.add_argument("disable-infobars")
            options.add_argument("window-size=1200,800")
        if platform.system() == "Linux":
            options.add_argument("no-sandbox")
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        return driver

    def get_images(self, class_: str):
        self.WAIT.until(EC.element_to_be_clickable((By.XPATH, self.button_xpath)))
        bs = BeautifulSoup(self.driver.page_source, 'lxml')
        # 找到背景图片和缺口图片的div
        img_div = bs.find_all(class_=class_)
        # 获取缺口背景图片url
        img_url = re.findall(r'background-image:\surl\("(.*?)"\)', img_div[0].get('style'))
        # 将图片格式存为 jpg 格式
        img_url = img_url[0].replace('webp', 'jpg')
        # 下载图片
        image = requests.get(img_url).content
        # 存放每个合成缺口背景图片的位置
        img_location_list = []
        for img in img_div:
            location = {'x': int(re.findall(r'background-position:\s(.*?)px\s(.*?)px;', img.get('style'))[0][0]),
                        'y': int(re.findall(r'background-position:\s(.*?)px\s(.*?)px;', img.get('style'))[0][1])}
            img_location_list.append(location)
        # 写入图片
        image_file = BytesIO(image)
        return image_file, img_location_list

    @staticmethod
    def merge_image(image_file: BytesIO, location_list: list):
        upper_half_list = []
        down_half_list = []
        image = Image.open(image_file)
        # 通过 y 的位置来判断是上半部分还是下半部分,然后切割
        for location in location_list:
            if location['y'] == -58:
                # 间距为10，y：58-116
                im = image.crop((abs(location['x']), 58, abs(location['x']) + 10, 116))
                upper_half_list.append(im)
            if location['y'] == 0:
                # 间距为10，y：0-58
                im = image.crop((abs(location['x']), 0, abs(location['x']) + 10, 58))
                down_half_list.append(im)
        # 创建一张大小一样的图片
        new_image = Image.new('RGB', (260, 116))
        # 粘贴好上半部分 y坐标是从上到下（0-116）
        offset = 0
        for im in upper_half_list:
            new_image.paste(im, (offset, 0))
            offset += 10
        # 粘贴好下半部分
        offset = 0
        for im in down_half_list:
            new_image.paste(im, (offset, 58))
            offset += 10

        return new_image

    @staticmethod
    def get_distance(bg_image: Image, fullbg_image: Image):
        # 阈值
        threshold = 200

        for i in range(60, bg_image.size[0]):
            for j in range(bg_image.size[1]):
                bg_pix = bg_image.getpixel((i, j))
                fullbg_pix = fullbg_image.getpixel((i, j))
                r = abs(bg_pix[0] - fullbg_pix[0])
                g = abs(bg_pix[1] - fullbg_pix[1])
                b = abs(bg_pix[2] - fullbg_pix[2])

                if r + g + b > threshold:
                    return i

    @staticmethod
    def get_track(distance: int, type_=1):
        if type_ == 1:
            return [distance]
        elif type_ == 2:
            track = []
            r = distance - 1
            while r:
                tmp = random.randint(-1, 10)
                if r > tmp:
                    track.append(tmp)
                    r -= tmp
                else:
                    track.append(r)
                    r = 0
            return track
        elif type_ == 3:
            track = []
            current = 0
            mid = distance * 3 / 4
            t = random.randint(2, 3) / 10
            v = 0
            while current < distance:
                if current < mid:
                    a = 2
                else:
                    a = -3
                v0 = v
                v = v0 + a * t
                move = v0 * t + 1 / 2 * a * t * t
                current += move
                track.append(round(move))
            return track
        else:
            raise Exception('type error')

    def drag_the_ball(self, track: list):
        knob = self.WAIT.until(
            EC.presence_of_element_located((By.XPATH, self.button_xpath)))
        ActionChains(self.driver).click_and_hold(knob).perform()
        # logger.info()(track)
        while track:
            x = random.choice(track)
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=random.randint(-5, 5)).perform()
            track.remove(x)
        time.sleep(0.1)
        imitate = ActionChains(self.driver).move_by_offset(xoffset=-1, yoffset=random.randint(-5, 5))
        time.sleep(0.015)
        imitate.perform()
        time.sleep(random.randint(6, 10) / 10)
        imitate.perform()
        time.sleep(0.04)
        imitate.perform()
        time.sleep(0.012)
        imitate.perform()
        time.sleep(0.019)
        imitate.perform()
        time.sleep(0.033)
        ActionChains(self.driver).move_by_offset(xoffset=1, yoffset=random.randint(-5, 5)).perform()
        ActionChains(self.driver).pause(random.randint(6, 14) / 10).release(knob).perform()

    def get_cookies(self):
        return self.driver.get_cookies()

    def get_url(self):
        return self.driver.current_url

    def close(self):
        self.driver.close()
        self.driver.quit()

    def send_keys(self, value: str, xpath: str):
        self.WAIT.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element = self.driver.find_element_by_xpath(xpath)
        element.clear()
        element.send_keys(value)

    def url_to_be(self, url: str):
        self.WAIT.until(EC.url_to_be(url))


if __name__ == '__main__':
    username = 'username'
    password = 'password'

    geetest = Geetest('https://passport.bilibili.com/login')
    geetest.send_keys(username, '//*[@id="login-username"]')
    geetest.send_keys(password, '//*[@id="login-passwd"]')
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
    cookies = Cookies.list_to_dict(cookies)
    logger.info(cookies)
    geetest.close()
    res = requests.get('https://space.bilibili.com/', cookies=cookies)
    logger.info(res.url)
