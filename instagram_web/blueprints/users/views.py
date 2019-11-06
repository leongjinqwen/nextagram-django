from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from models.user import User

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    new_user = User(email=email, username=username,
                    password=hashed_password)
    try:
        new_user.save()
        flash('Success!', "success")

    except Exception as e:
        print(e)
        flash("An error occurred!", "danger")

    return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
