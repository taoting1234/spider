import execjs


class FanyiHelper:
    @staticmethod
    def get_sign(keywords: str) -> str:
        with open('fanyi.js') as f:
            ctx = execjs.compile(f.read())
        return ctx.call('a', keywords)

    @staticmethod
    def detail_translate_result(raw: dict) -> str:
        return raw['trans'][0]['dst']
