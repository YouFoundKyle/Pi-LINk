## Getting Started with Django

### How to start the web app
1.  Make sure you have virtualenv and setup your environment.
    - Requires prerequisites
    - install with `sudo apt-get -y install python3-pip python3-virtualenv`
    - cd into web/ folder
    - Create venv
        - `virtualenv venv`
    - activate venv
        - `source venv/bin/activate`
    - install packages
        - `pip3 install -r requirements.txt`
2. To set up application:
    - For initial run or if there are changes:
        - python manage.py makemigrations
        - python manage.py migrate
    - Starts app on port 8000
        - python manage.py runserver
3. Access web app in browser
4. Sign up for account & login

### Documentation to check out:
- https://github.com/app-generator/django-gradient-able
- https://codedthemes.com/demos/admin-templates/gradient-able/bootstrap/doc/index.html