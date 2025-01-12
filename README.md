Project 12 - CRM
-
As part of the OpenClassroom "Python Application Developer" training program, this project is a CLI (Command Line Interface) application that helps with the management of clients, contracts, and events

Prerequisites :
-
Ensure to have the following installed on your system :

* Python 3.10 or higher
* Pipenv
* MySQL
* Sentry

Installation (windows)
-
In a terminal, clone this repository using :

    git clone https://github.com/Chillihache/Projet12.git

Create a database in MySQL and a django project in Sentry.

Clone the ".env.sample" file.

Rename your clone ".env"

Complete the informations in ".env".

Create a virtual environnement:

    python -m venv env

Activate the virtual environment :

    env\Scripts\activate.bat
    
Enter the project :

    cd Projet12

Install dependencies :

    pip install -r requirements.txt

To set up the data base :

    python manage.py makemigrations

    python manage.py migrate

Create the groups :

    python cli.py creategroups

Create a superuser to create the firsts users :

    python manage.py createsuperuser

Then, you can see all commands in commands.txt


