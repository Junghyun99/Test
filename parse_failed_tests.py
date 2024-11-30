import xml.etree.ElementTree as ET
import requests
import os

# Parse the JUnit XML result file
tree = ET.parse('report.xml')
root = tree.getroot()

# Extract failed test cases
failed_tests = []
for testcase in root.findall(".//testcase[failure]"):
    failed_tests.append(testcase.attrib["name"])

# Prepare Slack message
if failed_tests:
    message = f"Tests failed: {', '.join(failed_tests)}"
else:
    message = "No tests failed."

# Send to Slack
slack_webhook_url = os.getenv('SLACK_WEBHOOK')
slack_payload = {
    "text": f"Pytest Completed:\n- Status: failure\n- Branch: {os.getenv('GITHUB_REF_NAME')}\n- Commit: {os.getenv('GITHUB_SHA')}\n{message}"
}

requests.post(slack_webhook_url, json=slack_payload)