import requests
import os

import oauth2

UID = os.environ['42UID']
SECRET = os.environ['42UID']

# Create the client with your credentials
client = oauth2.Client("u-s4t2ud-a3460dc27a5dc4b8d1fbba961bfab6be66dc7eb02886000ce33e2b4c7976a0f6", "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", site="https://api.intra.42.fr")

# Get an access token
ACCESS_TOKEN = client.client_credentials.get_token()

# Function to retrieve data from the 42 API
def get_student_data(username):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"https://api.intra.42.fr/v2/users/{username}", headers=headers)
    student_data = response.json()
    return student_data

# Function to retrieve completed projects of a student from the 42 API
def get_completed_projects(username):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"https://api.intra.42.fr/v2/users/{username}/projects_users?filter[status]=finished", headers=headers)
    projects_data = response.json()
    return projects_data

# Get input username from user
username = input("Enter student username: ")

# Retrieve student data and completed projects using the 42 API
student_data = get_student_data(username)
completed_projects = get_completed_projects(username)

# Output student information and completed projects
print(f"Name: {student_data['displayname']}")
print(f"Email: {student_data['email']}")
print(f"Phone: {student_data['phone']}")
print(f"Completed projects:")
for project in completed_projects:
    print(f"\t{project['project']['name']} - final mark: {project['final_mark']}")