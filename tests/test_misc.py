import enchant


def test_get_version():
    version = enchant.get_enchant_version()
    assert type(version) == str


def test_get_user_config_dir():
    user_dir = enchant.get_user_config_dir()
    print(user_dir)
