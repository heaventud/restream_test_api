import pytest
import logging
from hamcrest.core import assert_that, equal_to
from hamcrest.library.number import greater_than
from config import Config
from lib.QaApi import Helper
from lib.Client import TestClient


@pytest.fixture(scope='session')
def test_config():
    return Config()


@pytest.fixture(scope="session")
def my_logger():
    # Initialize logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    handler = logging.FileHandler('test.log')
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)
    return logger


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


@pytest.fixture(autouse=True, scope='function')
def get_movies(my_logger, request):
    def _get_movies(device):
        my_logger.debug(f"Start {request.node.name}")
        client = TestClient(device_type=device)
        r = client.get_movies()
        if r.status_code != 200:
            my_logger.debug(f"{r.request.method} {r.request.url} ----> {r.status_code} {r.text}")
        else:
            my_logger.debug(f"{r.request.method} {r.request.url} ----> {r.status_code}")
        assert_that(r.status_code, equal_to(200))
        items = r.json()['items']
        assert_that(len(items), greater_than(0), f'There are no movies for {device}')
        my_logger.debug('\n'.join(str(x) for x in items))
        return items
    return _get_movies
