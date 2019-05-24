from bs4 import BeautifulSoup, NavigableString


class ZuccJwbHelper:
    @staticmethod
    def parse_article_list(raw: str) -> [dict]:
        bs = BeautifulSoup(raw, "lxml")
        res_list = list()
        for i in bs.find(class_="newslist").ul:
            if isinstance(i, NavigableString):
                continue
            res_list.append({
                'title': i.contents[0].contents[2].text,
                'url': "http://zuccjwb.zucc.edu.cn/" + i.contents[0].contents[2].attrs['href'],
                'time': i.contents[1].text
            })
        return res_list
