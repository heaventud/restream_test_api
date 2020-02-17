from lib.Wrapper import WrapSession


class TestClient:
    """This class allows access to the Restream API
    """
    def __init__(self, device_type=None, *args, **kwargs):
        self.session = WrapSession(prefix_url="http://tools.restream.ru:8889", *args, **kwargs)
        self.session.proxies.update({'http': 'http://127.0.0.1:8888'})
        # get token for device_type
        resp = self.session.post('/api/token', json={"device_type": device_type})
        resp.raise_for_status()
        self.token = resp.json().get('token')

    def get_movies(self):
        path = '/api/movies'
        self.session.headers = {
            'Accept': 'application/json',
            'X-TOKEN': self.token
        }
        resp = self.session.get(path)
        return resp

