from bs4 import BeautifulSoup


class JsxyHelper:
    @staticmethod
    def parse_article_list(raw: dict) -> list:
        res_list = list()
        for i in raw['datastore']['recordset']['record']:
            bs = BeautifulSoup(i, 'lxml')
            res_list.append({
                'title': bs.contents[0].contents[0].contents[0].contents[0].contents[0].contents[1].attrs['title'],
                'url': "http://jsxy.zucc.edu.cn" +
                       bs.contents[0].contents[0].contents[0].contents[0].contents[0].contents[1].attrs['href'],
                'time': bs.contents[0].contents[0].contents[0].contents[0].contents[1].contents[0][1:-1]
            })
        return res_list
