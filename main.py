from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
import pdfkit
import portfolio
import json

UID = "u-s4t2ud-a3460dc27a5dc4b8d1fbba961bfab6be66dc7eb02886000ce33e2b4c7976a0f6"
SECRET = "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"

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
    if response.status_code == 200:
        student_data = response.json()
        return student_data
    else:
        return None

# Function to retrieve completed projects of a student from the 42 API
def get_completed_projects(username):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"https://api.intra.42.fr/v2/users/{username}/projects_users?filter[status]=finished", headers=headers)
  
    projects_data = response.json()
    filtered_projects_data = [project for project in projects_data if project['validated?'] == True and "Piscine" not in project['project']['name']]
    return filtered_projects_data

# Define function to generate HTML from data
def generate_html(student_data, completed_projects):
    projects_html = ""
    for project in completed_projects:
      project_name = project['project']['name']
      final_mark = project['final_mark']
      projects_html += f"<tr><td class='project-name'>{project_name}</td><td class='final-mark'>{final_mark}</td></tr>"
    html = portfolio.html_template.format(name=student_data['displayname'], email=student_data['email'], phone=student_data['phone'], small_image_url = student_data['image']['versions']['small'], projects=projects_html)
    return html

def get_project_details(project_id):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"https://api.intra.42.fr/v2/projects/{project_id}", headers=headers)
    project_data = response.json()
    with open("output.txt", "w") as f:
      f.write(json.dumps(project_data, indent=4))
    return project_data

def print_projects(student_data, completed_projects):
  # Output student information and completed projects
  print(f"Name: {student_data['displayname']}")
  print(f"Email: {student_data['email']}")
  print(f"Phone: {student_data['phone']}")
  print(small_image_url)
  print(f"Completed projects:")
  for project in completed_projects:
    print(f"\t{project['project']['name']} - final mark: {project['final_mark']}")
    #project_details = get_project_details(project['project']['id'])
  
# Get input username from user
username = ""
while username != "exit":
  username = input("Enter student username: ")
  # Retrieve student data and completed projects using the 42 API
  student_data = get_student_data(username)
  if student_data is None:
        print(f"Error: User {username} not found.\n")
        continue
  completed_projects = get_completed_projects(username)
  small_image_url = student_data['image']['versions']['small']
  print(small_image_url)
  print_projects(student_data, completed_projects)
  html = generate_html(student_data, completed_projects)
  # Generate PDF from HTML using pdfkit
  # pdfkit.from_string(portfolio.html_template, f"{username}_projects.pdf")
  print()