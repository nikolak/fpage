# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, session, jsonify)

from fpage.utils import login_required
from fpage.extensions import login_manager
from fpage.user.models import User
from fpage.user.forms import RegisterForm
from fpage.utils import flash_errors


blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/login/", methods=['POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['username']).first()
        if u is None or not u.check_password(request.form['password']):
            return jsonify({"response": "error"})
        else:
            session['logged_in'] = True
            session['username'] = u.username
            if u.is_admin:
                session['admin']=True
            return jsonify({"response": "Logged in"})


@blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    if session.get('admin'):
        session.pop('admin', None)
    flash('You are logged out.', 'info')
    return redirect(url_for('submission.page'))
    # logout_user()
    # flash('You are logged out.', 'info')
    # return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                               email=form.email.data,
                               password=form.password.data,
                               active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('submission.page'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")