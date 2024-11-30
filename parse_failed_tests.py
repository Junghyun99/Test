import xml.etree.ElementTree as ET
import requests
import os
from collections import defaultdict

# Parse the JUnit XML result file
tree = ET.parse('report.xml')
root = tree.getroot()

# Group failed test cases by file
failed_tests_by_file = defaultdict(list)
for testcase in root.findall(".//testcase[failure]"):
    file_name = testcase.attrib.get("classname", "unknown_file")
    test_name = testcase.attrib["name"]
    failed_tests_by_file[file_name].append(test_name)

# Prepare Slack message
if failed_tests_by_file:
    message = "Failed Test Cases:\n"
    for file_name, tests in failed_tests_by_file.items():
        message += f"{file_name}:\n"
        for test in tests:
            message += f"- {test}\n"
else:
    message = "No tests failed."

# Send to Slack
slack_webhook_url = os.getenv('SLACK_WEBHOOK')
slack_payload = {
    "text": f"Pytest Completed:\n- Status: failure\n- Branch: {os.getenv('GITHUB_REF_NAME')}\n- Commit: {os.getenv('GITHUB_SHA')}\n\n{message}"
}

response = requests.post(slack_webhook_url, json=slack_payload)
response.raise_for_status()