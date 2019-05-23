import xmltodict


class XmlParser:
    @staticmethod
    def loads(s):
        res = xmltodict.parse(s)
        res = dict(res)
        return res

    @staticmethod
    def dumps(d):
        dd = {'xml': d}
        res = xmltodict.unparse(dd, full_document=False)
        return res
