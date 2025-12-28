def suggest_locator(page_source, failed_locator):
    """
    AI-assisted locator suggestion (stub).

    In future:
    - Send DOM to LLM
    - Ask for alternative locators
    - Return ranked suggestions
    """
    suggestions = [
        "By.ID: new-login-button",
        "By.CSS_SELECTOR: button[data-test='login-button']",
        "By.XPATH: //button[contains(text(),'Login')]"
    ]
    return suggestions
