# B.Nice
<img alt="Bnice landing screenshot" src="https://user-images.githubusercontent.com/26039401/47957503-b9d75280-dfae-11e8-98f6-a1e61c1039c9.png" width="50%">

[![Build Status](https://travis-ci.org/Tomasz-Kluczkowski/Bnice.svg?branch=master)](https://travis-ci.org/Tomasz-Kluczkowski/Bnice) [![Coverage Status](https://coveralls.io/repos/github/Tomasz-Kluczkowski/Bnice/badge.svg?branch=master&service=github)](https://coveralls.io/github/Tomasz-Kluczkowski/Bnice?branch=master)

## More You, Less Chores - Get your child to help you at home

## What is this application about?

In this project I am aiming at converting a wallchart where we record our kid's good and bad behaviour into a web app.
The main idea is for your kid to collect points and get stars as a reward. You decide what they get for a star :).

## What tech used?

The app is written using **Python / Django** and a few helpful libraries which I am mentioning to pay credit to the authors:
- bootstrap (get your grid done in no time: <https://getbootstrap.com/>)
- django-bootstrap4 (excellent way of making forms look good, it's a godsend, check it out at: <https://github.com/zostera/django-bootstrap4>)
- django-static-precompiler (use scss without any watchers and other complications, big thx to this project: <https://github.com/andreyfedoseev/django-static-precompiler>).
- pytest-django (test without too much boilerplate code: <https://pytest-django.readthedocs.io/en/latest/>)
- python-decouple (keep secret settings secret :) <https://github.com/henriquebastos/python-decouple>)
- factory_boy (get the database objects made for you easily <http://factoryboy.readthedocs.io/en/latest/>)
- django-debug-toolbar (makes digging in your site so much faster: <https://django-debug-toolbar.readthedocs.io/en/stable/>)

## You can make this app better

This is a side project and a way to get better in Django / Front end technologies and experiment. Anyone is welcome to help - there is
a great amount of stuff that can be added / improved and I have so little time :(.
Instructions are meant for people who never worked with Git / Django etc. but if they are still too complicated please
help me and make them better for new starters :). 
Anyone who wants to try to set this up on Windows has my special blessings :).
Check out issues at: <https://github.com/Tomasz-Kluczkowski/Bnice/issues>.

## Installation

If you would like to play with the code in this app you can install it:

- Open terminal

### Get a local copy of the project:
```bash
git clone https://github.com/Tomasz-Kluczkowski/Bnice.git #  Clone the project to your computer.
git clone git@github.com:Tomasz-Kluczkowski/Bnice.git # If you use ssh keys.
```
### Or make a local copy for contributing:

Please fork the project to your own Github account and then clone your own version instead of mine.
**How to fork / clone:**
- Login to **your** Github account.
- Navigate to: <https://github.com/Tomasz-Kluczkowski/Bnice>
- Click Fork (Fork like icon in top right corner with a number next to it). This will take only a short while. 
- Go to **your** Github account and choose your copy of Bnice repo there.
- Click green icon Clone or Download, copy the address provided in the field - will be similar to: <https://github.com/your-account-name/Bnice.git>
- in terminal use what you copied and issue a command:
```bash
git clone https://github.com/<your-account-name>/Bnice.git
git@github.com:<your-account-name>/Bnice.git # If you use ssh keys
```

I recommend using an ssh key for all your Git authorisation needs. They are very easy to set up and no more hassle with passwords :).
Check instructions here: <https://help.github.com/articles/connecting-to-github-with-ssh/>

### Install project's dependencies

- Install prerequisites for sass (currently django-static-precompiler which is used to compile scss does not work with DartSass so npm install sass 
will not work and unfortunately you need ruby sass).
```bash
sudo apt-get install ruby ruby-dev
sudo gem install sass
```

- Install project's requirements.
```bash
cd Bnice/ #  Navigate to the project's root.
virtualenv -p python3 venv #  Create a virtual environment for the project.
source venv/bin/activate #  Activate the environment.
pip install -r requirements.txt # Install all dependencies.
```

### Configure project's variables

- Create a file for the app's environment variables.
```bash
touch .env
```

Then edit the .env file.
```bash
gedit .env
```

Add the following lines:
```
DEBUG=True
SECRET_KEY=secret
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1, 0.0.0.0 # Or any internal network IP address you want to use for the server, comma separated values
```
- Save and close the .env file.

### Migrate database and run server

- Now we are ready to apply migrations and launch the site.
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

## Access Bnice app

Simply go to your browser and type 127.0.0.1:8000

### Accessing website on other devices

If you need to check site on other devices on your network you will have to add the local IP address of the host to the 
list of allowed hosts in settings.py.
Then you can access this site from any device on your network by typing: [host IP address]:8000

Example variable in .env file:
```
ALLOWED_HOSTS=192.168.1.156, 127.0.0.1
```
- 192.168.1.156:8000 will access site hosted at 192.168.1.156 on your local network.
This is useful when testing behaviour of site on mobiles / tablets etc to confirm your browser's inspection tool is not faking it.

## Testing

We use tox to tun tests and pytest-django to write them (this is the main exercise to go away from the default UnitTest).
To run tests simply type:
```bash
tox
```
- After tests inspect coverage - go to htmlcov folder that should appear after tox finished running. Use index.html to navigate
between coverage of project's files. If anything was missed in testing coverage report will show it in red 
(completely missed or yellow - partially missed :).

## How to use the app?

- Simply sign up and create your account. This account will be classified as a parent account.
- You should see an icon of a profile - navigate to the dashboard.
- Create your first child profile in dashboard. Notice that all child profiles are users like you but with read-only access.
- Your child can edit their profile (well not the star points / password for obvious reasons)
- Add smileys and oopsies :) when they deserve them.
- Give details of the child account if you wish so to your kid so they can view their progress!