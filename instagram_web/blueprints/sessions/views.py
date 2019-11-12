import peewee as pw
from flask import Blueprint, flash, redirect, render_template, request, url_for,session,escape
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_required,login_user,logout_user,current_user

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    # make get request to display log in form
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    user = User.get_or_none(User.email==request.form.get('email'))
    if user:
    # if user found in database
        result = check_password_hash(user.password, request.form.get('password'))
        if result :
            # loggin user
            # session["user_id"] = user.id
            login_user(user)
            flash("Successfully signed in.","success")
            return redirect(url_for('users.show',username=user.username))
        else :
            flash("Wrong password, try again.","danger")
            return render_template('sessions/new.html')
    else:
    # if no user found in database
        flash('No account found.',"danger")
        return render_template('sessions/new.html')

@sessions_blueprint.route('/delete',methods=['POST'])
@login_required
def destroy():
    # session.pop('user_id', None)
    logout_user()
    flash("Successfully logged out.",'success')
    return redirect(url_for('sessions.new'))

