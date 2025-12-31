import pytest
from pages.login_page import LoginPage
from utils.logger import get_logger

@pytest.mark.smoke
def test_valid_login(driver):
    logger = get_logger(__name__)
    logger.info("Starting valid login test")

    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    logger.info("Valid login successful")
    assert "inventoory" in driver.current_url

@pytest.mark.regression
def test_invalid_login_shows_error(driver):
    logger = get_logger(__name__)
    logger.info("Negative test validation with invalid credentials")

    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_user", "wrong_password")

    error_text = login_page.get_error_message()
    logger.info("Error message validation successful")
    assert "Username and password do not match" in error_text

