from lib.Wrapper import WrapSession


class TestClient:
    """This class allows access to the Restream API
    """
    def __init__(self, logger, prefix_url="", device_type=None, *args, **kwargs):
        self.session = WrapSession(prefix_url=prefix_url, *args, **kwargs)
        self.logger = logger
        # get token for device_type
        resp = self.session.post('/api/token', json={"device_type": device_type})
        self.logger.debug(
            f"{resp.request.method} {resp.request.url} {resp.request.body} ---> {resp.status_code}")
        resp.raise_for_status()
        self.token = resp.json().get('token')

    def get_movies(self):
        path = '/api/movies'
        self.session.headers = {
            'Accept': 'application/json',
            'X-TOKEN': self.token
        }
        r = self.session.get(path)
        # logging success and response
        if r.status_code != 200:
            self.logger.debug(f"{r.request.method} {r.request.url} ----> {r.status_code} {r.text}")
        else:
            self.logger.debug(f"{r.request.method} {r.request.url} ----> {r.status_code}")
        return r

