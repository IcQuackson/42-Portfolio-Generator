from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from jinja2 import Environment, FileSystemLoader
import requests
import pdfkit
import portfolio
import json

UID = "u-s4t2ud-a3460dc27a5dc4b8d1fbba961bfab6be66dc7eb02886000ce33e2b4c7976a0f6"
SECRET = "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"

env = Environment(loader=FileSystemLoader('.'))
#template = env.get_template('teste.html')

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
    
def get_user_skills(user_id):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"https://api.intra.42.fr/v2/users/{user_id}/cursus_users", headers=headers)
    cursus_users = response.json()
    if cursus_users:
        skills = cursus_users[0]['skills']
        return skills
    else:
        return []


# Function to retrieve completed projects of a student from the 42 API
def get_completed_projects(username):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"https://api.intra.42.fr/v2/users/{username}/projects_users?filter[status]=finished", headers=headers)
  
    projects_data = response.json()
    filtered_projects_data = [project for project in projects_data if project['validated?'] == True and "Piscine" not in project['project']['name']]
    return filtered_projects_data


# Define function to generate HTML from data

def generate_html(student_data, completed_projects, output_file):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('teste.html')

    projects_data = []
    for project in completed_projects:
        project_data = {
            'name': project['project']['name'],
            'final_mark': project['final_mark'],
        }
        projects_data.append(project_data)

    html = template.render(
        student_name=student_data['displayname'],
        email=student_data['email'],
        phone=student_data['phone'],
        small_image_url=student_data['image']['versions']['small'],
        completed_projects=projects_data
    )

    with open(output_file, 'w') as f:
        f.write(html)

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
    print(f"Small image URL: {student_data['image']['versions']['small']}")
    print(f"Completed projects:")
    for project in completed_projects:
        print(f"\t{project['project']['name']} - final mark: {project['final_mark']}")
        project_details = get_project_details(project['project']['id'])
        project_description = project_details['project_sessions'][0]['description']
        print(f"\t\tDescription: {project_description}")
        objectives = project_details['project_sessions'][0]['objectives']
        objectives_str = ', '.join(objectives)  # Convert the list of objectives to a string
        print(f"\t\tSkills: {objectives_str}")

    # Print user skills
    user_skills = get_user_skills(student_data['id'])
    for skill in user_skills:
        level = skill['level']
        new_value = 0
        if 0 <= level < 2:
            new_value = 1
        elif 2 <= level < 4:
            new_value = 2
        elif 4 <= level < 6:
            new_value = 3
        elif 6 <= level < 8:
            new_value = 4
        elif 8 <= level <= 10:
            new_value = 5
        skill['new_value'] = new_value
        print(f"\nSkill: {skill['name']} - Level: {level} - New Value: {new_value}")
    return user_skills




  
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
  output_file = f"{username}_portfolio.html"
  html = generate_html(student_data, completed_projects, output_file)

  # Generate PDF from HTML using pdfkit
  #pdfkit.from_string(portfolio.html_template, f"{username}_projects.pdf")
  print()