# Planner-Flask
A personal application to help me plan events and meetings

This project was built as a final project for Harvard's CS50 3 month course

## Contributing
To contribute to this project you can just clone this repo or submit a pull request

## Features included with this project
* AWS github Pipeline with CI/CD capabilities
* Theme setting
* Email sending
* Account Creation
* Authentication
* Event Creation
* Event Listing
* Unauthenticated user Event Creation
* Toast notifications
* and Many more

## Setting up the project
You will need an **API key** from [mailgun]("https://signup.mailgun.com/new/signup") in order to send emails

### >After Cloning the repository to your local computer run the following commands

#### Windows CMD or Powershell run the following
```
pip install -r requirements **or** pip3 install -r requirements 
set FLASK_APP application.py
set FLASK_ENV development
set EMAIL_KEY MAILGUN_API_KEY
```

#### WSL, Ubuntu or Mac OS
```
pip install -r requirements **or** pip3 install -r requirements 
export FLASK_APP=application.py
export FLASK_ENV=development
export EMAIL_KEY= MAILGUN_API_KEY
```

### If you enjoyed this project please leave a follow or a star⭐
