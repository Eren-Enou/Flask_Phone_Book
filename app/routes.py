from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import AddressForm
from app.models import Address

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/address', methods=["GET", "POST"])
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
        new_address = Address(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
        flash(f"Thank you {new_address.first_name} for adding your address!", "success")
        return redirect(url_for('index'))
    return render_template('address.html', form=form)
