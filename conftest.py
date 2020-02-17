import pytest
from lib.QaApi import Helper


@pytest.fixture(scope='session')
def api_helper():
    return Helper()


@pytest.fixture(scope='session')
def service_maker(api_helper):
    def _service_maker(**kwargs):
        resp = api_helper.create_service(**kwargs)
        return resp.json()['id']
    return _service_maker


@pytest.fixture(scope='session')
def movie_maker(api_helper):
    def _movie_maker(**kwargs):
        id_movie = api_helper.create_movie(**kwargs)
        # check that movie is created successfully
        api_helper.get_movie(id_movie)
        return id_movie
    return _movie_maker
