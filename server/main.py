from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, render_template, url_for
import requests
# import pdfkit
# import portfolio
import json
import math
import time

app = Flask(__name__, static_url_path='/assets', static_folder='static')

UID = "u-s4t2ud-a3460dc27a5dc4b8d1fbba961bfab6be66dc7eb02886000ce33e2b4c7976a0f6"
SECRET = "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"

env = Environment(loader=FileSystemLoader('.'))
html_file = "templates/template.html"

# Create a client object with your credentials
client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)
oauth.fetch_token(token_url="https://api.intra.42.fr/oauth/token", client_id=UID, client_secret=SECRET)

# Get an access token
ACCESS_TOKEN = oauth.access_token

@app.route('/')
def index():
	return render_template('index.html')

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
	time.sleep(0.5)
	projects_data = response.json()
	filtered_projects_data = [project for project in projects_data if project['validated?'] == True and "Piscine" not in project['project']['name'] and "Exam" not in project['project']['name']]
	return filtered_projects_data

def get_project_details(project_id):
	headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
	response = requests.get(f"https://api.intra.42.fr/v2/projects/{project_id}", headers=headers)
	time.sleep(0.5)
	project_data = response.json()
	return project_data


# Define function to generate HTML from data
def generate_html(student_data, completed_projects, html_file, url_for):
	env = Environment(loader=FileSystemLoader('.'))
	template = env.get_template(html_file)

	projects_data = []
	for project in completed_projects:
		project_details = get_project_details(project['project']['id'])
		try:
			project_description = project_details['project_sessions'][0]['description']
		except:
			project_description = ""
		try:
			objectives = project_details['project_sessions'][0]['objectives']
		except:
			project_description = ""
		project_data = {
			'name': project['project']['name'],
			'final_mark': project['final_mark'],
			'description': project_description,
			'objectives': objectives
		}
		projects_data.append(project_data)

	user_skills = get_user_skills(student_data['id'])
	for skill in user_skills:
		level = skill['level']
		new_value = math.ceil(level / 2)
		skill['new_value'] = new_value

	html = template.render(
		student_name=student_data,
		email=student_data['email'],
		phone=student_data['phone'],
		small_image_url=student_data['image']['versions']['medium'],
		completed_projects=projects_data,
		skills=user_skills,
		url_for=url_for
	)

	return html

def get_user_skills(user_id):
	headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
	response = requests.get(f"https://api.intra.42.fr/v2/users/{user_id}/cursus_users", headers=headers)
	cursus_users = response.json()
	if cursus_users:
		skills = cursus_users[0]['skills']
		return skills
	else:
		return []

@app.route('/generate_portfolio', methods=['POST'])
def generate_portfolio():
	username = request.form['username']

	student_data = get_student_data(username)
	if student_data is None:
		return render_template('index.html', error=f"User {username} not found.")

	completed_projects = get_completed_projects(username)
	output_file = f"{username}_portfolio.html"
	html = generate_html(student_data, completed_projects, html_file, url_for)
	return html

if __name__ == '__main__':
	app.run(debug=True)
