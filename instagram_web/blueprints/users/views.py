import peewee as pw
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required,current_user,login_user
from dj.models.user import User
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    valid_email = request.args.get('v_e')

    return render_template('users/new.html', valid_email=valid_email)


@users_blueprint.route('/', methods=['POST'])
def create():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    new_user = User(
        email=email,
        username=username,
        password=password)

    v_e = False

    try:
        if new_user.save():
            login_user(new_user)
            flash('Successfully created a user!', "success")
            v_e = True

        else:
            flash("An error occurred!", "danger")

    except pw.IntegrityError as e:
        print(e)

    return redirect(url_for("users.new", v_e=v_e))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.objects.get(username=username)
    return render_template("users/show.html",user=user)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.objects.get(id=id)
    if (current_user.role == "admin" or current_user.id==user.id):
        return render_template("users/edit.html",user=user)
    else:
        flash(f"You are not allowed to update {user.username}'s profile",'danger')
        return render_template("users/show.html",user=current_user)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.objects.get(id=id)
    if current_user == user :
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.password = request.form.get('password')
        if user.save():
            flash("Successfully updated.","success")
            return redirect(url_for('users.edit',id=id))
        else:
            errors = user.errors
            for error in errors:
                flash(error,"danger")
            flash("Can not update profile.","danger")
            return render_template("users/edit.html",user=user)
    else:
        flash(f"You are not allowed to update {user.username}'s profile",'danger')
        return render_template("users/edit.html",user=user)

@users_blueprint.route('/<id>/picture', methods=['POST'])
@login_required
def update_picture(id):
    # get file from request
    file = request.files.get("user_file")
    # if no file in request
    if not file:
        flash("Please choose a file.","danger")
        return render_template('images/new.html')
    # if file in request
    file.filename = secure_filename(file.filename)
    output = upload_file_to_s3(file)
    # if no image link get from upload function mean upload is unsuccessful
    if not output:
        flash("Unable to upload file, try again.","danger")
        return render_template('images/new.html')
    # if img link return, mean upload successful
    else:
        # get current user
        user = User.update(profile_picture = output).where(User.id == current_user.id)
        # save profile image link in user class
        user.execute()
        flash("Profile picture updated","success")
        return redirect(url_for('users.show', username=current_user.username))