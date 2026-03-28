import pytest
from server import app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def clubs_data():
    return loadClubs()


@pytest.fixture
def competitions_data():
    return loadCompetitions()
