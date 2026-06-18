from __future__ import annotations

import platform
import sys
from pathlib import Path

import pytest

from config.settings import Settings, build_settings


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--env", action="store", default=None, help="Environment config name from config/environments")
    parser.addoption("--base-url", action="store", default=None, help="Application base URL")
    parser.addoption("--api-url", action="store", default=None, help="API base URL")
    parser.addoption("--user-id", action="store", default=None, help="Candidate user id")
    parser.addoption("--browser", action="store", default=None, help="Browser name. Supported: chrome")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser tests in headless mode")
    parser.addoption("--timeout", action="store", type=int, default=None, help="Default explicit wait timeout")


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    resolved_settings = build_settings(
        env=pytestconfig.getoption("--env"),
        base_url=pytestconfig.getoption("--base-url"),
        api_url=pytestconfig.getoption("--api-url"),
        user_id=pytestconfig.getoption("--user-id"),
        browser=pytestconfig.getoption("--browser"),
        headless=pytestconfig.getoption("--headless"),
        timeout=pytestconfig.getoption("--timeout"),
    )
    _write_allure_environment(pytestconfig, resolved_settings)
    return resolved_settings


def _write_allure_environment(pytestconfig: pytest.Config, settings: Settings) -> None:
    allure_dir = pytestconfig.getoption("--alluredir")
    if not allure_dir:
        return

    environment_file = Path(allure_dir) / "environment.properties"
    environment_file.parent.mkdir(parents=True, exist_ok=True)
    environment_file.write_text(
        "\n".join(
            [
                f"Environment={settings.env}",
                f"Base URL={settings.base_url}",
                f"API URL={settings.api_url}",
                f"Browser={settings.browser}",
                f"Headless={settings.headless}",
                f"Timeout={settings.timeout}",
                f"Python={sys.version.split()[0]}",
                f"OS={platform.platform()}",
            ]
        ),
        encoding="utf-8",
    )
