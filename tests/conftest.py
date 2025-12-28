import os
import pytest
from datetime import datetime
from core.browser_manager import BrowserManager
from utils.logger import get_logger


logger = get_logger("TestLifecycle")

@pytest.fixture
def driver():
    driver = BrowserManager.get_chrome_driver()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    logger.info(f"STARTED test: {item.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.failed:
            error_reason = str(report.longrepr)
            if hasattr(report.longrepr, "reprcrash"):
                logger.error(f"Reason: {report.longrepr.reprcrash.message}")
            else:
                logger.error(f"Reason: {report.longrepr}")

            driver = item.funcargs.get("driver")
            if driver:
                screenshots_dir = "logs/screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)

                screenshot_name = f"{item.name}_{datetime.now().strftime('%H%M%S')}.png"
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)

                driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")

        elif report.passed:
            logger.info(f"PASSED test: {item.name}")



