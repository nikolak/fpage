===============================
flaskPage
===============================

Social news (HN/reddit-like) site made with Python and flask


Quickstart
----------

::

    git clone https://github.com/Nikola-K/fpage
    cd fpage
    pip install -r requirements/dev.txt
    export FPAGE_ENV='dev'
    python manage.py createdb
    python manage.py runserver


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``models``, and ``db``.

Development / Production Environments
-------------------------------------

Configuration environements are handled through the FPAGE_ENV system environment variable.

To switch to the development environment, set ::

    export FPAGE_ENV="dev"

To switch to the production environment, set ::

    export FPAGE_ENV="prod"