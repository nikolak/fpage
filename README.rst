===============================
fpage
===============================

A social news web app similar to reddit written in flask/python


Quickstart
----------

::

    git clone https://github.com/Nikola-K/fpage
    cd fpage
    pip install -r requirements/dev.txt
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``FPAGE_ENV`` environment variable is set to ``"prod"``.

Admin User
----------

Create your account and visit ``yourdomain.com/admin`` - if no admin exists current user will be assigned as admin.

This can not be changed later other than accessing database directly and changing value.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commmands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.