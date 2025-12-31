import json
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

HISTORY_FILE = Path("ai_utils/flaky_history.json")


def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def update_test_history(test_name, status):
    history = load_history()

    if test_name not in history:
        history[test_name] = {
            "history": [],
            "last_seen": None
        }

    history[test_name]["history"].append(status)
    history[test_name]["last_seen"] = datetime.now().isoformat()

    save_history(history)

def process_junit_results(report_path="reports/results.xml"):
    tree = ET.parse(report_path)
    root = tree.getroot()

    for testcase in root.iter("testcase"):
        test_name = f"{testcase.get('classname')}::{testcase.get('name')}"

        if testcase.find("failure") is not None:
            update_test_history(test_name, "FAIL")
        else:
            update_test_history(test_name, "PASS")

def detect_flaky_tests(min_runs=3):
    history = load_history()
    flaky_tests = {}

    for test, data in history.items():
        outcomes = data["history"]

        if len(outcomes) < min_runs:
            continue

        if "FAIL" in outcomes and "PASS" in outcomes:
            flaky_tests[test] = outcomes

    return flaky_tests

if __name__ == "__main__":
    process_junit_results()
    flaky = detect_flaky_tests()

    if flaky:
        print("\nPOTENTIALLY FLAKY TESTS\n" + "-" * 40)
        for test, history in flaky.items():
            print(f"{test} -> {history}")
    else:
        print("No flaky tests detected.")

