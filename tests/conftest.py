import pytest
import random


@pytest.fixture
def setup_test_tc_002(api_helper):
    api_helper.delete_movies()
    yield


@pytest.fixture(params=['tv', 'mobile', 'stb'])
def setup_test_tc_003(request, service_maker, movie_maker):
    service_id = service_maker(name='Basic Service', price=20000, device_types=[request.param])
    movie_id = movie_maker(name='King Lion', start_date=2019, end_date=2021, services=[service_id])
    yield (request.param, service_id, movie_id)


@pytest.fixture(scope='module')
def setup_test_tc_005(service_maker, movie_maker):
    """"""
    servs = []
    for dev in ['tv', 'mobile', 'stb']:
        service_id = service_maker(name=f'Good Service for {dev}', price=20000, device_types=[dev])
        servs.append(service_id)
    id_movie = movie_maker(name='Alladin', start_date=2020, end_date=2022, services=servs)
    yield id_movie


@pytest.fixture
def setup_test_tc_006(service_maker, movie_maker):
    """Creates several services for 1 device type and then creates movie for each service"""
    import random
    device = 'stb'
    service_ids = [service_maker(name=f'service {random.randint(99, 9999)}', device_types=[device])
                   for _ in range(3)]
    movie_ids = [movie_maker(name=f'movie {random.randint(99, 9999)}', start_date=2020, end_date=2022, services=[s])
                 for s in service_ids]
    yield device, movie_ids


@pytest.fixture(params=['tv', 'mobile', 'stb'])
def setup_test_tc_007(service_maker, movie_maker, request):
    """"""
    service_id = service_maker(name='Basic Service', device_types=[request.param])
    movie_maker(name='Фильм', start_date=2018, end_date=2019, services=[service_id])
    yield (request.param, service_id)


@pytest.fixture(scope='module')
def setup_test_tc_008(service_maker, movie_maker):
    """Creates 1 service for all devices and relates it with a movie"""
    devices = ['tv', 'mobile', 'stb']
    service_id = service_maker(name='Basic Service', device_types=devices)
    movie_id = movie_maker(name=f'Фильм {random.randint(99, 9999)}', start_date=2020, end_date=2021, services=[service_id])
    yield movie_id


@pytest.fixture(params=['tv'])
def setup_test_tc_009(service_maker, movie_maker, api_helper, request):
    """Creates many movies for test"""
    api_helper.delete_movies()
    num = 10
    service_id = service_maker(name=f'Service {random.randint(99, 999)}', device_types=[request.param])
    ids = []
    for _ in range(num):
        movie_id = movie_maker(name=f'Фильм {random.randint(99, 9999)}', start_date=2020, end_date=2021,
                               services=[service_id])
        ids.append(movie_id)
    yield (request.param, ids)


@pytest.fixture(params=['tv', 'mobile', 'stb'])
def setup_test_tc_010(movie_maker, api_helper, request):
    """"""
    api_helper.delete_movies()
    res1 = api_helper.create_service(name=f'Service {random.randint(99, 9999)}', device_types=[request.param])
    service_id = res1.json().get('id', '0')
    test_movie = {
        "name": f"Film {random.randint(99, 9999)}",
        "description": "description",
        "start_date": 2020,
        "end_date": 2021,
        "services": [service_id]
    }
    movie_id = movie_maker(**test_movie)
    test_movie['services'] = [res1.request.body]
    test_movie['id'] = movie_id
    yield (request.param, movie_id, test_movie)

