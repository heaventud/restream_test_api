import uuid
import pytest
from lib.Client import TestClient
from hamcrest.core import assert_that, equal_to, all_of, not_none
from hamcrest.library.number import greater_than
from hamcrest.library.collection import has_items
from hamcrest.library.text import contains_string


@pytest.mark.parametrize('token', [
    '',
    uuid.uuid1()
])
def test_client_receives_403_when_invalid_token(token):
    """Verify that client cant get movies without token
    """
    client = TestClient('tv')
    client.token = str(token)
    r = client.get_movies()
    assert_that(r.status_code, equal_to(403))
    assert_that(r.json()['message'], contains_string("'Токен не найден'"))


@pytest.mark.parametrize('device', [
    'tv',
    'mobile',
    'stb'
])
def test_client_receives_200_when_movies_not_found(device):
    """Verify that client receives ok status and empty list of movies,
    if movies are not found
    """
    client = TestClient(device)
    r = client.get_movies()
    assert_that(r.status_code, equal_to(200))
    assert_that(r.json()['items'], equal_to([]))


def test_client_gets_movies_only_for_platform(create_movies_before_test):
    """
    """
    device, service_id = create_movies_before_test
    client = TestClient(device_type=device)
    r = client.get_movies()
    assert_that(r.status_code, equal_to(200))
    items = r.json()['items']
    assert_that(len(items), greater_than(0),
                f'There are no movies for {device}')
    item = [True for x in items if service_id in x.get('services', [])]
    assert_that(item, not(equal_to([])), f'Not found movie for platform {device}')


@pytest.mark.parametrize('device', [
    'mobile'
])
def test_movie_structure_in_response_json(service_maker, movie_maker, device):
    """Verify response structure
    """
    service_id = service_maker(name='basic_service', device_types=[device])
    movie_maker(name='Best of the best', start_date=2019, end_date=2021, services=[service_id])
    client = TestClient(device_type=device)
    r = client.get_movies()
    assert_that(r.status_code, equal_to(200))
    items = r.json().get('items', None)
    assert_that(items, not_none(), f'No one film found for {device}')
    assert_that(next(iter(items), None), all_of(not_none(),
                                                has_items('id', 'name', 'description', 'start_date',
                                                          'end_date', 'services')))


@pytest.mark.parametrize('device', [
    'tv',
    'mobile',
    'stb'
])
def test_client_receives_movie_when_it_has_several_services(create_services_before_test, device):
    """Verify Client receives movie for his device successfully if it includes into several services
    """
    id_movie = create_services_before_test
    client = TestClient(device_type=device)
    r = client.get_movies()
    assert_that(r.status_code, equal_to(200))
    items = r.json().get('items', None)
    assert_that(items, not_none(), f'No one film found for {device}')
    movie = next((item for item in items if item.get('id', 0) == id_movie), None)
    assert_that(movie, not_none(), f'Movie with {id_movie} is not found\n')


def test_client_receives_movies_from_several_services(services_before_test):
    """Verify client  receives successfully various movies from various services related with one device
    """
    device, movies = services_before_test
    client = TestClient(device_type=device)
    r = client.get_movies()
    assert_that(r.status_code, equal_to(200))
    items = r.json().get('items', None)
    all_movies = [item.get('id', 0) for item in items]
    assert_that(all_movies, has_items(*movies))
