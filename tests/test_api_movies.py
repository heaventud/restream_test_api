import uuid
import pytest
from lib.Client import TestClient
from hamcrest.core import assert_that, equal_to, all_of, not_none
from hamcrest.library.number import greater_than
from hamcrest.library.collection import has_items, has_item
from hamcrest.library.text import contains_string


@pytest.mark.tc_001
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


@pytest.mark.tc_002
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


@pytest.mark.tc_003
def test_client_gets_movies_only_for_platform(setup_test_tc_003, get_movies):
    """
    """
    device, service_id = setup_test_tc_003
    items = get_movies(device)
    item = [True for x in items if service_id in x.get('services', [])]
    assert_that(item, not(equal_to([])), f'Not found movie for platform {device}')


@pytest.mark.tc_004
@pytest.mark.parametrize('device', [
    'mobile'
])
def test_movie_structure_in_response_json(service_maker, movie_maker, get_movies, device):
    """Verify response structure
    """
    service_id = service_maker(name='basic_service', device_types=[device])
    movie_maker(name='Best of the best', start_date=2019, end_date=2021, services=[service_id])
    items = get_movies(device)
    assert_that(next(iter(items), None), all_of(not_none(),
                                                has_items('id', 'name', 'description', 'start_date',
                                                          'end_date', 'services')))


@pytest.mark.tc_005
@pytest.mark.parametrize('device', [
    'tv',
    'mobile',
    'stb'
])
def test_client_receives_movie_when_it_has_several_services(setup_test_tc_005, get_movies, device):
    """Verify Client receives movie for his device successfully if it includes into several services
    """
    id_movie = setup_test_tc_005
    items = get_movies(device)
    movie = next((item for item in items if item.get('id', 0) == id_movie), None)
    assert_that(movie, not_none(), f'Movie with {id_movie} is not found\n')


@pytest.mark.tc_006
def test_client_receives_movies_from_several_services(setup_test_tc_006, get_movies):
    """Verify client receives successfully various movies from various services which are related with one device
    """
    device, movies = setup_test_tc_006
    items = get_movies(device)
    all_movies = [item.get('id', 0) for item in items]
    assert_that(all_movies, has_items(*movies))


@pytest.mark.tc_007
def test_client_not_receives_movie_if_its_out_of_date(setup_test_tc_007, get_movies):
    """Client doesn't receive movie if it is out of date
    """
    device, old_movie = setup_test_tc_007
    items = get_movies(device)
    all_movies = [item.get('id', 0) for item in items]
    assert_that(all_movies, not(has_item(old_movie)))

