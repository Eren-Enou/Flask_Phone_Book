from app import app, db
from flask import render_template, redirect, url_for, flash
# from fake_data import posts
from app.forms import SignUpForm, LoginForm, AddressForm, SearchForm
from app.models import User, Address
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/', methods=["GET", "POST"])
def index():
    addresses = Address.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.search_term.data
        addresses = db.session.execute(db.select(Address).where((Address.address.ilike(f"%{search_term}%")) | (Address.phone_number.ilike(f"%{search_term}%")))).scalars().all()
    return render_template('index.html', addresses=addresses, form=form)


@app.route('/address', methods=["GET", "POST"])
@login_required
def address():
    # Create an instance of the form (in the context of the current request)
    form = AddressForm()
    # Check if the form was submitted and that all of the fields are valid
    if form.validate_on_submit():
        # If so, get the data from the form fields
        print('Validated Form')
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, phone_number, address)
        new_address = Address(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, user_id=current_user.id)
        flash(f"Thank you {new_address.first_name} for adding your address!", "success")
        return redirect(url_for('index'))
    return render_template('address.html', form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Create an instance of the form (in the context of the current request)
    form = SignUpForm()
    # Check if the form was submitted and that all of the fields are valid
    if form.validate_on_submit():
        # If so, get the data from the form fields
        print('Hooray our form was validated!!')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(first_name, last_name, email, username, password)
        # Check to see if there is already a user with either username or email
        check_user = db.session.execute(db.select(User).filter((User.username == username) | (User.email == email))).scalars().all()
        if check_user:
            # Flash a message saying that user with email/username already exists
            flash("A user with that username and/or email already exists", "warning")
            return redirect(url_for('signup'))
        # If check_user is empty, create a new record in the user table
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f"Thank you {new_user.username} for signing up!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated :)')
        username = form.username.data
        password = form.password.data
        print(username, password)
        # Check if there is a user with username and that password
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            # If the user exists and has the correct password, log them in
            login_user(user)
            flash(f'You have successfully logged in as {username}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))

@app.route('/edit/<address_id>', methods=["GET", "POST"])
@login_required
def edit_address(address_id):
    form = AddressForm()
    address_to_edit = Address.query.get_or_404(address_id)
    # Make sure that the Address author is the current user
    if address_to_edit.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('index'))

    # If form submitted, update Address
    if form.validate_on_submit():
        # update the post with the form data
        address_to_edit.first_name = form.first_name.data
        address_to_edit.last_name = form.last_name.data
        address_to_edit.address = form.address.data
        address_to_edit.phone_number = form.phone_number.data
        # Commit that to the database
        db.session.commit()
        flash(f"{address_to_edit.address} has been edited!", "success")
        return redirect(url_for('index'))

    # Pre-populate the form with Address To Edit's values
    form.first_name.data = address_to_edit.first_name
    form.last_name.data = address_to_edit.last_name
    form.address.data = address_to_edit.address
    form.phone_number.data = address_to_edit.phone_number
    return render_template('edit.html', form=form, address=address_to_edit)


@app.route('/delete/<address_id>')
@login_required
def delete_address(address_id):
    address_to_delete = Address.query.get_or_404(address_id)
    if address_to_delete.author != current_user:
        flash("You do not have permission to delete this address", "danger")
        return redirect(url_for('index'))

    db.session.delete(address_to_delete)
    db.session.commit()
    flash(f"{address_to_delete.address} has been deleted", "info")
    return redirect(url_for('index'))