import enchant


def test_get_user_config_dir():
    """
    Scenario:
      Either broker.get_user_config_dir() works
      (enchant >= 2.0), or it throws AttributeError
      (enchant < 2.0)

    """
    try:
        user_dir = enchant.get_user_config_dir()
        assert user_dir
    except AttributeError:
        assert True
