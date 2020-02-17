# Help Desk

### Purpose
This is a Django based web application that will allow users on an LDAP service to view and submit help desk tickets to support staff. Support staff may assign or resolve these tasks and an email will notify the user of their resolution. 

### Installation
This application requires Python 3.7. The following instructions can be used to run a development server. For production, it is advised to follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04).

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

 * Create groups with the create_groups command  
 `python manage.py create_groups`

 * (Optional) Test users can be created with the create_fake_users command.  
 `python manage.py create_fake_users`

 * Run the server.   
 `python manage.py runserver [ADDRESS:PORT] --settings=helpdesk.settings.dev`

### License
All rights reserved by the Bernalillo County District Attorney's Office.
