from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import os

UID = os.environ['42UID']
SECRET = os.environ['42SECRET']

# Create a client object with your credentials
client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)
oauth.fetch_token(token_url="https://api.intra.42.fr/oauth/token", client_id=UID, client_secret=SECRET)

# Get an access token
ACCESS_TOKEN = oauth.access_token

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
  if project['validated?'] == True and "Piscine" not in project['project']['name']:
    print(f"\t{project['project']['name']} - final mark: {project['final_mark']}")