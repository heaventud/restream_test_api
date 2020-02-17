from lib.Wrapper import WrapSession
from qa_tools.utils import date_converter
import time


class Helper:
    """This class allows access to the QA API
    """
    def __init__(self, *args, **kwargs):
        self.s = WrapSession(prefix_url="http://tools.restream.ru:8889", *args, **kwargs)
        self.s.headers.update({'Accept': 'application/json'})
        self.s.proxies.update({'http': 'http://127.0.0.1:8888'})

    def create_movie(self, **opts):
        """Method creates movie with options
        """
        path = "/qa/movies"
        json = {
            "id": opts.get('id', 0),
            "name": opts.get('name', ""),
            "description": opts.get("description", ''),
            "start_date": int(date_converter(opts['start_date'] if opts.get('start_date', 0) else 0)),
            "end_date": int(date_converter(opts['end_date']) if opts.get('end_date', 0) else 0),
            "services": opts.get('services', [])
        }
        r = self.s.post(path, json=json)
        r.raise_for_status()
        return r.json().get('id', None)

    def create_service(self, **opts):
        """Method creates service with options
        """
        path = '/qa/services'
        json = {
            "id": opts.get('id', 0),
            "name": opts.get('name', ""),
            "description": opts.get("description", ''),
            "price": opts.get("price", 0),
            "device_types": opts.get('device_types', [])
        }
        r = self.s.post(path, json=json)
        r.raise_for_status()
        return r

    def get_movie(self, id_movie):
        """Method checks if movie was created successfully
        """
        path = f'/qa/movies/{id_movie}'
        i = 0
        while i < 5:
            r = self.s.get(path)
            if r.status_code == 200:
                break
            i += 1
            time.sleep(1)
        else:
            raise AssertionError(f'Movie with id {id_movie} is not created')

    def delete_services(self):
        """Method deletes all services
        """
        path = '/qa/services'
        r = self.s.delete(path)
        r.raise_for_status()

    def delete_movies(self):
        """Method deletes all movies
        """
        path = '/qa/movies'
        r = self.s.delete(path)
        r.raise_for_status()
