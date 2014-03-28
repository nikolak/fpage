# -*- coding: utf-8 -*-
'''Helper utilities and decorators.'''
from functools import wraps

from flask import flash, session, url_for
from werkzeug.utils import redirect


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)


def login_required(test):
    '''Decorator that makes a view require authentication.'''

    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.', 'warning')
            return redirect(url_for('submission.page'))

    return wrap