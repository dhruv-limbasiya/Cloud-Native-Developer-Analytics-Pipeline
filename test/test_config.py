from src.core.config_loader import ConfigLoader


def test_config_loaded():

    config = ConfigLoader().get_config()

    assert config is not None


def test_github_section_exists():

    config = ConfigLoader().get_config()

    assert "github" in config


def test_request_timeout_exists():

    config = ConfigLoader().get_config()

    assert "request_timeout" in config["github"]


def test_retry_count_exists():

    config = ConfigLoader().get_config()

    assert "retry_count" in config["github"]


def test_per_page_exists():

    config = ConfigLoader().get_config()

    assert "per_page" in config["github"]