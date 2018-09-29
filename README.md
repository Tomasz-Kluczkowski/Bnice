# B.Nice
[![Build Status](https://travis-ci.org/Tomasz-Kluczkowski/Bnice.svg?branch=master)](https://travis-ci.org/Tomasz-Kluczkowski/Bnice) [![Coverage Status](https://coveralls.io/repos/github/Tomasz-Kluczkowski/Bnice/badge.svg?branch=master&service=github)](https://coveralls.io/github/Tomasz-Kluczkowski/Bnice?branch=master)

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

## Help is needed

This is a side project and a way to get better in Django / Front end technologies. Anyone is welcome to help - there is
a great amount of stuff that can be improved and I have so little time :(. 
Check out issues at: <https://github.com/Tomasz-Kluczkowski/Bnice/issues>.

## Installation

If you would like to play with the code in this app you can install it:

In terminal:
------------

### If you just want a copy of the project:
```
git clone https://github.com/Tomasz-Kluczkowski/Bnice.git #  Clone the project to your computer.
git@github.com:Tomasz-Kluczkowski/Bnice.git # If you use ssh keys.
```
### If you would like to contribute:

Please fork the project to your own Github account and then clone your own version instead of mine.
- Login to **your** Github account.
- Navigate to:
<https://github.com/Tomasz-Kluczkowski/Bnice>
- Click Fork (Fork icon in top right corner). 
- Go to **your** Github account and choose the Bnice repo there.
- Click green icon Clone or Download, copy the address provided in the field - will be similar to: <https://github.com/your-account-name/Bnice.git>
- in terminal use what you copied and issue a command:
```
git clone https://github.com/<your-account-name>/Bnice.git
git@github.com:<your-account-name>/Bnice.git # If you use ssh keys.
```

### Follow the rest of the instructions

- Install prerequisites for sass (currently django-static-precompiler does not work with DartSass so npm install sass 
will not work and unfortunately you need ruby sass... hopefully this will get fixed soon).
```
sudo apt-get install ruby ruby-dev
sudo gem install sass
```

- Install project requirements.
```
cd Bnice/ #  Navigate to the project's root.
virtualenv -p python3 venv #  Create a virtual environment for the project.
source venv/bin/activate #  Activate the environment.
pip install -r requirements.txt # Install all dependencies.
touch .env # To create a new file where we will keep the secret settings of the app.
```
Add .env file to your .gitignore file (if it's not already there).
```
gedit .env # To edit the .env file.
# Add the following line:
DEBUG=True #  Great for any testing.
```
- Save and close the .env file.
- Now we are ready to apply migrations and launch the site.
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 --settings=Bnice.development_settings # To run the server.
```
- Additional settings if you would like to deploy (for example to heroku) for staging/live testing.
    Normally the environment variables in Heroku override those settings but if you want to use a different platform or
    just test using a virtual machine simulating a server you need to set up at least the secret key properly to test
    with production settings. For development settings and test settings the secret_key='secret' already. 
    - Go to <https://www.miniwebtool.com/django-secret-key-generator/>
    - Generate a new secret key for yourself. Once you add it in .env file it will be read automatically for you.<br>
    Make sure you **DO NOT** add .env file to the files that are synced to your repo!<br>
    The secret key is meant to be secret after all...
```
gedit .env # To edit the .env file.
# Add the following line:
DEBUG=True #  Great for any testing - set to False if checking with production settings locally. Use heroku's environment 
variables to override this in production.
SECRET_KEY=<here paste your own 50 characters long random key> # Use heroku's environment variables to override this in 
production.
```


## Accessing website

Simply go to your browser and type 127.0.0.1:8000

## Accessing website on other devices

If you need to check site on other devices on your network you will have to add the local IP address of the host to the 
list of allowed hosts in settings.py.
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