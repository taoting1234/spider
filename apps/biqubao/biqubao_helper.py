import re

from bs4 import BeautifulSoup


class BiqubaoHelper:
    @staticmethod
    def parse_content(raw: str) -> str:
        bs = BeautifulSoup(raw, "lxml")
        r = bs.find(id='content').text
        r = r.replace('    ', '\n    ')
        r = r[1:]
        return r

    @staticmethod
    def parse_chapter_list(raw: str) -> [dict]:
        bs = BeautifulSoup(raw, "lxml")
        r = bs.find(id='list')
        rr = []
        for i in r.contents[1].contents[3:-1]:
            rr.append({
                'title': i.a.text,
                'chapter_id': re.findall(r'/(\d*)\.html', i.a.attrs['href'])[0]
            })
        return rr
