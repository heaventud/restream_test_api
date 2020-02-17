import pytest


@pytest.fixture(params=['tv', 'mobile', 'stb'])
def setup_test_tc_003(request, service_maker, movie_maker):
    service_id = service_maker(name='Basic Service', price=20000, device_types=[request.param])
    movie_maker(name='King Lion', start_date=2019, end_date=2021, services=[service_id])
    yield (request.param, service_id)


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
