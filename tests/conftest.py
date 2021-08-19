import pytest
from enchant import Broker, get_enchant_version


def pytest_sessionstart(session: pytest.Session):
    enchant_version = get_enchant_version()
    print("Running with Enchant C library at version", enchant_version)


@pytest.fixture(autouse=True, scope="session")
def ensure_en_us_dict():
    broker = Broker()
    en_us_available = broker.dict_exists("en_US")
    if not en_us_available:
        pytest.exit("The tests need an en_US dictionary to run properly")
