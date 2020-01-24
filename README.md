# Help Desk

### Purpose
This is a Django based web application that will allow users on an LDAP service to view and submit help desk tickets to support staff. Support staff may assign or resolve these tasks and an email will notify the user of their resolution. 

### Installation
This application requires Python 3.7. For the time being, this application can be run in its Alpha state with Django's runserver command. The following instructins can be used for deployment.

 * Create your virtual environment using Python 3.7.  
 `python3 -m venv env`  

 * Run your virtual environment.  
 `source venv/bin/activate`

 * Install dependencies using pip.  
 `pip install -r requirements.txt`

 * Set up the database.  
 `python manage.py migrate`

 * Collect static resources  
 `python manage.py collectstatic`

 * Copy .env file and fill with appropriate values  
 `cp .env.example .env`  
 `vim .env`

 * (Optional) Groups and test users can be created with the create_fake_users command.  
 `python manage.py create_fake_users`

 * (Optional) Set DEBUG to False in helpdesk/settings.py.

 * Run the server. (insecure flag will allow runserver to access static resources in Debug mode)  
 `python manage.py runserver [ADDRESS:PORT] --insecure`

### License
All rights reserved by the Bernalillo County District Attorney's Office.
