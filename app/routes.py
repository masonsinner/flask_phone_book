from app import app, db, models
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import EnterAddress, EditAddress
from app.forms import SignUpForm, LoginForm
from app.models import User, Address
from sqlalchemy import or_

app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    addresses = Address.query.all()
    return render_template('index.html', addresses=addresses)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('index'))


@app.route('/search_address', methods=["GET", "POST"], endpoint='search_address')
@login_required
def search_address():
    form = EnterAddress()

    if form.validate_on_submit():
        # Get information from the form
        search_term = form.search_term.data

        # Perform search query
        addresses = Address.query.filter(
            or_(
                Address.ad_first_name.ilike(f'%{search_term}%'),
                Address.ad_last_name.ilike(f'%{search_term}%')
            )
        ).all()

        return render_template('show_address.html', addresses=addresses, User=User)

    return redirect(url_for('index'))


@app.route('/address_book', methods=["GET", "POST"], endpoint='address_book')
@login_required
def enter_address():
    form = EnterAddress()

    if form.validate_on_submit():
        # Get information from the form
        ad_first_name = form.first_name.data
        ad_last_name = form.last_name.data
        phone_number = form.phone_number.data
        street_address = form.street_address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        email = form.email.data

        address = Address(
            ad_first_name=ad_first_name,
            ad_last_name=ad_last_name,
            phone_number=phone_number,
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            email=email,
            submitter=current_user.id
        )

        db.session.add(address)
        db.session.commit()

        flash('Address added successfully', 'success')

        return redirect(url_for('index'))

    # Perform search query
    search_term = request.args.get('search_term', '')
    addresses = Address.query.filter(
        or_(
            Address.ad_first_name.ilike(f'%{search_term}%'),
            Address.ad_last_name.ilike(f'%{search_term}%')
        )
    ).all()

    return render_template('address_book.html', form=form, addresses=addresses)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    # Create an instance of the SignUpForm class
    form = SignUpForm()
    # Check if the request is POST and the form is valid
    if form.validate_on_submit():
        print('HOORAY OUR FORM IS VALIDATED!')
        # If valid, get the data from the form
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(first_name, last_name, username, email, password)
        # Query the user table to see if there are any users with that username or email
        user_check = User.query.filter((User.username == username) | (User.email == email)).all()
        # If there are any users with username or email, flash a warning message
        if user_check:
            flash('A user with that username and/or email already exists', 'danger')
            return redirect(url_for('signup'))
        # Create a new user
        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        # flash a message saying user has signed up
        flash(f"{username} has signed up for the blog!", 'success')
        # Redirect back to the home page
        return redirect(url_for('index'))
    # Send that instance to the html as context
    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated!')
        username = form.username.data
        password = form.password.data
        print(username, password)
        # Check to see if there is a user with that username
        user = User.query.filter_by(username=username).first()
        # If there is a user AND the password matches that user's hashed password
        if user is not None and user.check_password(password):
            # log the user in via login_user function
            login_user(user)
            flash(f'{username} has successfully logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username and/or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/edit_address/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_address(id):
    address = Address.query.get_or_404(id)

    if address.submitter != current_user.id:
        flash("Sorry, you are not authorized to edit this address.", "danger")
        return redirect(url_for('index'))

    form = EditAddress()

    if form.validate_on_submit():
        address.ad_first_name = form.first_name.data
        address.ad_last_name = form.last_name.data
        address.street_address = form.street_address.data
        address.city = form.city.data
        address.state = form.state.data
        address.zip_code = form.zip_code.data
        address.phone_number = form.phone_number.data
        address.email = form.email.data
        db.session.commit()

        flash("You edited the address successfully.", "success")
        return redirect(url_for('index'))

    elif request.method == 'GET':
        form.first_name.data = address.ad_first_name
        form.last_name.data = address.ad_last_name
        form.street_address.data = address.street_address
        form.city.data = address.city
        form.state.data = address.state
        form.zip_code.data = address.zip_code
        form.phone_number.data = address.phone_number
        form.email.data = address.email

    return render_template('edit_address.html', form=form, address=address)


@app.route('/delete_address/<int:address_id>', methods=["POST"])
@login_required
def delete_address(address_id):
    address = Address.query.get(address_id)
    if address is None:
        flash('Address not found', 'danger')
        return redirect(url_for('index'))

    if address.submitter != current_user.id:
        flash('Sorry, you are not authorized to delete this address', 'danger')
        return redirect(url_for('index'))

    db.session.delete(address)
    db.session.commit()
    flash('Address removed successfully', 'success')
    return redirect(url_for('index'))


@app.route('/user_addresses/<int:user_id>')
@login_required
def user_addresses(user_id):
    user = User.query.get(user_id)
    addresses = Address.query.filter_by(submitter=user_id).all()
    return render_template('user_addresses.html', user=user, addresses=addresses)

