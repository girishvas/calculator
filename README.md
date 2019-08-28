# django-simple-calculator

Simple application for calcution numbers.
Role based arithmatic operator.

## Steps need to be perform

git clone the repository then

Make virtual environment with python3 and activate it:
```
virtualenv env --python=python3

source ./env/bin/activate

cd calculator

pip install -r requirement.txt

```
Database is alog with this repository user also adde to the database

```
python manage.py runserver

http://127.0.0.1:8000/api/docs/
```

Site will availabel here

can perform all operations here.

## things to be noted

there are two types of user available, normal user and admin user

```
	Admin User

	username  : admin
	password  : admin123

	Normal User

	username  : email@email.com
	password  : password
```

In "/api/v1/operations/simpleoperation/"

please try to add the operation as the following

```
add, sub, mult, div, pow, sqrt, fact
```

For report ("/api/v1/operations/report/") and download ("/api/v1/operations/download/") plesae pass the parameters

```
today, weekly, monthly, yearly, all
```

try to check the api's with both the user.