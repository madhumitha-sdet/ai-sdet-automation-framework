import os
import pytest
from datetime import datetime
from core.browser_manager import BrowserManager


@pytest.fixture
def driver():
    driver = BrowserManager.get_chrome_driver()
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = "logs/screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            screenshot_name = f"{item.name}_{datetime.now().strftime('%H%M%S')}.png"
            screenshot_path = os.path.join(screenshots_dir, screenshot_name)

            driver.save_screenshot(screenshot_path)
            

