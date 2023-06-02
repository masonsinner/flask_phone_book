from app import app 
from flask import render_template, redirect, url_for, flash
from app.forms import EnterAddress

app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/address_book', methods=["GET", "POST"], endpoint='address_book')
def signup():
    #Create var form 
    form = EnterAddress()
    #Post part 
    if form.validate_on_submit():
        print('Good job!')
        #get information for flash
        first_name = form.first_name.data
        last_name = form.last_name.data
        address = form.address.data
        email = form.email.data
        phone_number = form.phone_number.data
        print(f"{first_name} {last_name} {address}, {email},{ phone_number} has been added to the address book!")
        #flash message for confirmed submit 
        flash(f"You registered {first_name} {last_name}, and they stay on {address}.\n To get ahold of them you can call {phone_number}, or email {email}")
        #take them back home 
        return redirect(url_for('index'))
    #send that information to html as context 
    return render_template('address_book.html', form=form)