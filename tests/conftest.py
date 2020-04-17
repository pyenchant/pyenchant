import pytest
from enchant import Broker


@pytest.fixture(autouse=True, scope="session")
def ensure_en_us_dict():
    broker = Broker()
    en_us_available = broker.dict_exists("en_US")
    if not en_us_available:
        pytest.exit("The tests need an en_US dictionary to run properly")
