import peewee as pw

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.user import User

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    valid_email = bool(int(request.args.get('valid_email')))
    print('valid', valid_email)
    print('valid type', type(valid_email))

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

    try:
        if new_user.save():
            flash('Successfully created a user!', "success")
            ve = 1
        else:
            flash("An error occurred!", "danger")
            ve = 0

    except pw.IntegrityError as e:
        print(e)

    return redirect(url_for("users.new", ve=ve))


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
