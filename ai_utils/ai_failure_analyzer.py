import xml.etree.ElementTree as ET
from pathlib import Path


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


def main():
    report_path = "reports/results.xml"
    failures = parse_junit_report(report_path)

    if not failures:
        print("No test failures detected.")
        return

    print("Detected test failures:\n")
    for failure in failures:
        print(
            f"- {failure['test_name']} "
            f"({failure['error_type']}): {failure['message']}"
        )


if __name__ == "__main__":
    main()
