Task List App
=============

A Django-based Task Management App that allows users to manage tasks, track progress, and prioritize efficiently. Features include user-specific task views, admin access, and optional dashboard and calendar functionalities.


Requirements:
-------------

- [python 3.10.3](https://python.org/downloads/>)
- [pre-commit](https://pre-commit.com/>)
- [virtualenv](https://virtualenv.pypa.io/en/stable/>)

Getting Started
---------------

1. Clone the repo:

```
$ git clone https://github.com/g1039/task-list-app.git
$ cd task-list-app
```

2. Setup the virtualenv

```
$ virtualenv ve
$ source ve/bin/activate
```

3. Install requirements:

```
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
$ pre-commit install
```

4. Setup database

```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

5. Run tests

```
$ pytest
```

6. Start the application

```
$ python manage.py runserver
```

You can now access the demo site on http://localhost:8000
