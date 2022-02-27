from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

#from config.development import DATABASES

app = Flask(__name__)

# WEBSITE_HOSTNAME exists only in production environment
if not 'WEBSITE_HOSTNAME' in os.environ:
   # local development, where we'll use environment variables
   print("Loading config.development and environment variables from .env file.")
   app.config.from_object('azureproject.development')
else:
   # production
   print("Loading config.production.")
   app.config.from_object('azureproject.production')

print('DATABASE_URI = ' + str(app.config.get('DATABASE_URI')))
app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)
from restaurant_review.models import Guest
db.create_all()
db.session.commit()

# initialize database migration management
migrate = Migrate(app, db)

@app.route('/')
def view_registered_guests():
    from restaurant_review.models import Guest
    guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)


@app.route('/register', methods=['GET'])
def view_registration_form():
    return render_template('guest_registration.html')


@app.route('/register', methods=['POST'])
def register_guest():
    from restaurant_review.models import Guest
    name = request.form.get('name')
    email = request.form.get('email')

    guest = Guest(name, email)
    db.session.add(guest)
    db.session.commit()

    return render_template(
        'guest_confirmation.html', name=name, email=email)

if __name__ == '__main__':
   app.run()