# B.Nice
[![Build Status](https://travis-ci.org/Tomasz-Kluczkowski/Bnice.svg?branch=master)](https://travis-ci.org/Tomasz-Kluczkowski/Bnice)

More You, Less Chores - Get your child to help you at home

## What is this application about?

In this project I am aiming at converting a wallchart where we record our kid's good and bad behaviour into a web app.
The main idea is for your kid to collect points and get stars as a reward. You decide what they get for a star :).

## What tech is used?

The app is written using **Python / Django** and a few helpful libraries which I am mentioning to pay credit to the authors:
- bootstrap (get your grid done in no time: <https://getbootstrap.com/>)
- django-bootstrap4 (excellent way of making forms look good, it's a godsend, check it out at: <https://github.com/zostera/django-bootstrap4>)
- django-static-precompiler (use scss without any watchers and other complications, big thx to this project: <https://github.com/andreyfedoseev/django-static-precompiler>).
- pytest-django (test without too much boilerplate code: <https://pytest-django.readthedocs.io/en/latest/>)
- python-decouple (keep secret settings secret :) <https://github.com/henriquebastos/python-decouple>)
- factory_boy (get the database objects made for you easily <http://factoryboy.readthedocs.io/en/latest/>)
- django-debug-toolbar (makes digging in your site so much faster: <https://django-debug-toolbar.readthedocs.io/en/stable/>)

## Installation

If you would like to play with the code in this app you can install it:

In terminal:
------------

### If you just want a copy of the project:
```
git clone https://github.com/Tomasz-Kluczkowski/Bnice.git #  Clone the project to your computer.
```
### If you would like to contribute:

Please fork the project to your own Github account and then clone your own version instead of mine.
- Login to your Github account.
- Navigate to:
<https://github.com/Tomasz-Kluczkowski/Bnice>
- Click Fork (Icon in top right corner). 
- Go to your Github account and choose the Bnice repo there.
- Click green icon Clone or Download, copy the address provided in the field - will be similar to: <https://github.com/your-account-name/Bnice.git>
- in terminal use what you copied and issue a command:
```
git clone https://github.com/your-account-name/Bnice.git
```

### Follow the rest of the instructions

```
cd Bnice/ #  Navigate to the project's root.
virtualenv -p python3 Bnice_env #  Create a virtual environment for the project.
source activate Bnice_env/ #  Activate the environment.
pip install -r requirements.txt # Install all dependencies.
touch .env # To create a new file where we will keep the secret settings of the app.
```
- Go to <https://www.miniwebtool.com/django-secret-key-generator/>
- Generate a new secret key for yourself. Once you add it in .env file it will be read automatically for you.<br>
Make sure you **DO NOT** add .env file to the files that are synced to your repo!<br>
Add .env file to your .gitignore file.
The secret key is meant to be secret after all...
```
gedit .env # To edit the .env file.
# Add the following line:
SECRET_KEY=<here paste your own 50 characters long random key>
DEBUG=True #  Great for any testing.
```
- Save and close the .env file.
- Now we are ready to apply migrations and launch the site.
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 # To run the server.
```
## Accessing website

Simply go to your browser and type 127.0.0.1:8000

## Accessing website on other devices

If you need to check site on other devices on your network you will have to add the local IP address of the host to the list of allowed hosts in settings.py.
Then you can access this site from any device on your network by typing: [host IP address]:8000

Example:
```
ALLOWED_HOSTS = ["192.168.1.156",
                 "127.0.0.1",
                 ]
```
- 192.168.1.156:8000 will access site hosted at 192.168.1.156 on your local network.
This is useful when testing behaviour of site on mobiles / tablets etc to confirm chrome inspection tool is not faking it.

## How to use the app?

- Simply sign up and create your account. This account will be classified as a parent account.
- You should see an icon of a profile - navigate to the dashboard.
- Create your first child profile in dashboard. Notice that all child profiles are users like you but with read-only access.
- Your child can edit their profile (well not the star points / password for obvious reasons)
- Add smileys and oopsies :) when they deserve them.
- Give details of the child account if you wish so to your kid so they can view their progress!


