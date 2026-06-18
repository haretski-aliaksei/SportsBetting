from __future__ import annotations

from pathlib import Path

import allure
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    screenshots_dir = Path("reports/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshots_dir / f"{item.name}.png"
    browser.save_screenshot(str(screenshot_path))

    allure.attach.file(
        str(screenshot_path),
        name="Failure screenshot",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(
        browser.page_source,
        name="Page source at failure",
        attachment_type=allure.attachment_type.HTML,
    )
    allure.attach(
        f"URL: {browser.current_url}\nTitle: {browser.title}",
        name="Browser state at failure",
        attachment_type=allure.attachment_type.TEXT,
    )
