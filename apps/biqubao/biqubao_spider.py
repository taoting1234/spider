from apps.biqubao.biqubao_helper import BiqubaoHelper
from apps.biqubao.biqubao_http import BiqubaoHttp


class BiqubaoSpider:
    @staticmethod
    def get_chapter_list(novel_id: int) -> [dict]:
        """
        获取章节（https://www.biqubao.com/book/18569/）
        :param novel_id: 小说id（18569）
        :return: 章节列表
        """
        url = 'https://www.biqubao.com/book/{}/'.format(novel_id)
        res = BiqubaoHttp().get(url=url)
        return BiqubaoHelper.parse_chapter_list(res.text)

    @staticmethod
    def get_content(novel_id: int, chapter_id: int) -> str:
        """
        获取小说（https://www.biqubao.com/book/18569/7789986.html）
        :param novel_id: 小说id（18569）
        :param chapter_id: 章节id（7789986）
        :return: 小说内容
        """
        url = 'https://www.biqubao.com/book/{}/{}.html'.format(novel_id, chapter_id)
        res = BiqubaoHttp().get(url=url)
        return BiqubaoHelper.parse_content(res.text)


if __name__ == '__main__':
    a = BiqubaoSpider.get_chapter_list(18569)
    print(a)
