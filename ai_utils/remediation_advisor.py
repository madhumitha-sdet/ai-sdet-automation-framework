
def suggest_remediation(classified_failures):
    """
    Generate remediation suggestions based on failure categories.

    AI is used as an advisory system.
    Suggestions must be reviewed and applied manually.
    """

    suggestions = {}

    if "locator_issues" in classified_failures:
        suggestions["locator_issues"] = [
            "Prefer stable attributes like data-test or aria-label.",
            "Avoid absolute XPaths; use relative locators.",
            "Verify DOM changes and update Page Object locators."
        ]

    if "timing_issues" in classified_failures:
        suggestions["timing_issues"] = [
            "Replace hard waits with explicit waits (WebDriverWait).",
            "Wait for element visibility instead of presence.",
            "Increase timeout only where genuinely needed."
        ]

    if "assertion_issues" in classified_failures:
        suggestions["assertion_issues"] = [
            "Avoid strict text matches when UI content is dynamic.",
            "Assert stable identifiers instead of full strings.",
            "Validate state changes instead of UI text where possible."
        ]

    if "environment_issues" in classified_failures:
        suggestions["environment_issues"] = [
            "Check browser/driver compatibility.",
            "Stabilize headless execution settings in CI.",
            "Retry failed setup steps only for infra failures."
        ]

    return suggestions
