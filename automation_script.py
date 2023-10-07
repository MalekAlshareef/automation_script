import os
import time
import requests
import json
from datetime import datetime

# Configuration settings
error_directory = 'path/to/error/files'
jira_base_url = 'https://your-jira-instance.com'
jira_username = 'your-jira-username'
jira_password = 'your-jira-api-token'
project_key = 'PROJECTKEY'
issue_type = 'Bug'
log_file = 'error_ticket_log.txt'

# Function to create an error ticket in JIRA
def create_jira_error_ticket(error_message):
    try:
        # Prepare the JIRA issue payload
        issue_payload = {
            'fields': {
                'project': {'key': project_key},
                'issuetype': {'name': issue_type},
                'summary': 'Error Ticket',
                'description': error_message
            }
        }

        # Send a POST request to create the JIRA issue
        response = requests.post(
            f'{jira_base_url}/rest/api/2/issue/',
            json=issue_payload,
            auth=(jira_username, jira_password)
        )

        if response.status_code == 201:
            return json.loads(response.text)['key']
        else:
            return None

    except Exception as e:
        print(f"Failed to create JIRA ticket: {str(e)}")
        return None

# Main loop to monitor for error files
while True:
    for error_file in os.listdir(error_directory):
        if error_file.endswith('.log'):
            error_file_path = os.path.join(error_directory, error_file)

            # Capture error details (e.g., from a log file)
            with open(error_file_path, 'r') as log_file:
                error_message = log_file.read()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Create a JIRA error ticket
            ticket_id = create_jira_error_ticket(error_message)

            # Log the ticket creation
            with open(log_file, 'a') as log:
                log.write(f"Timestamp: {timestamp}\n")
                log.write(f"Error Message: {error_message}\n")
                if ticket_id:
                    log.write(f"JIRA Ticket ID: {ticket_id}\n")
                else:
                    log.write("Failed to create JIRA ticket.\n")
                log.write("\n")

            # Remove the error file after processing (optional)
            os.remove(error_file_path)

    # Add a delay before checking for new errors (e.g., check every 60 seconds)
    time.sleep(60)
