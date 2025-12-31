import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
from ai_utils.remediation_advisor import suggest_remediation
from ai_utils.flaky_test_tracker import detect_flaky_tests
import os



def parse_junit_report(report_path: str):
    """
    Parse JUnit XML report and extract failed test cases.
    """
    report_file = Path(report_path)

    if not report_file.exists():
        raise FileNotFoundError(f"JUnit report not found: {report_path}")

    tree = ET.parse(report_file)
    root = tree.getroot()

    failures = []

    for testcase in root.iter("testcase"):
        failure = testcase.find("failure")
        if failure is not None:
            failures.append(
                {
                    "test_name": testcase.get("name"),
                    "class": testcase.get("classname"),
                    "error_type": failure.get("type", "Unknown"),
                    "message": failure.get("message", "").strip(),
                }
            )

    return failures


def classify_failures(failures):
    """
    Group failures by root cause.
    """
    categories = defaultdict(list)

    for failure in failures:
        message = failure["message"].lower()
        error_type = failure["error_type"].lower()

        if "no such element" in message or "unable to locate element" in message:
            categories["locator_issues"].append(failure)

        elif "timeout" in message or "timed out" in message:
            categories["timing_issues"].append(failure)

        elif "assert" in message or "assertionerror" in error_type:
            categories["assertion_issues"].append(failure)

        elif "sessionnotcreatedexception" in error_type or "chrome" in message:
            categories["environment_issues"].append(failure)

        else:
            categories["other_issues"].append(failure)

    return categories


def print_summary(classified_failures):
    """
    Print a human-readable summary of failures.
    """
    print("\nFAILURE SUMMARY\n" + "-" * 50)

    for category, items in classified_failures.items():
        print(f"\n{category.upper()} ({len(items)} tests)")
        for item in items:
            print(
                f" - {item['test_name']} "
                f"({item['error_type']}): {item['message']}"
            )

def is_ai_enabled():
    return os.getenv("ENABLE_AI", "false").lower() == "true"


def main():
    report_path = "reports/results.xml"

    # Step 1: Parse failures from JUnit report
    failures = parse_junit_report(report_path)

    if not failures:
        print("No test failures detected.")
        return

    # Step 2: Detect flaky tests (post-run, history based)
    flaky_tests = detect_flaky_tests()

    if flaky_tests:
        print("\nFLAKY TESTS DETECTED (Excluded from analysis)")
        print("-" * 50)
        for test_name, history in flaky_tests.items():
            print(f"{test_name} -> {history}")

    # Step 3: Filter out flaky failures
    stable_failures = [
        failure for failure in failures
        if failure["test_name"] not in flaky_tests
    ]

    if not stable_failures:
        print("\nAll failures are from flaky tests. No stable failures to analyze.")
        return

    # Step 4: Classify only stable failures
    classified = classify_failures(stable_failures)

    print_summary(classified)

    # Step 5: Generate remediation suggestions
    remediation = suggest_remediation(classified)

    print("\nREMEDIATION SUGGESTIONS\n" + "-" * 50)
    for category, actions in remediation.items():
        print(f"\n{category.upper()}")
        for action in actions:
            print(f" - {action}")

if __name__ == "__main__":
    main()
