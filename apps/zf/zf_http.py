from libs.http import Http


class ZfHttp(Http):
    def __init__(self):
        super().__init__()
        self.sess.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        self.sess.headers['Content-Type'] = 'application/x-www-form-urlencoded'
