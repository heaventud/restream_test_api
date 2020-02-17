import requests as r
from urllib.parse import urljoin


class WrapSession(r.Session):
    """Wrap class for default Session
    """
    def __init__(self, prefix_url=None, *args, **kwargs):
        super(WrapSession, self).__init__(*args, **kwargs)
        self.prefix_url = prefix_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(WrapSession, self).request(method, url, *args, **kwargs)
