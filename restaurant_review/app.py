from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from sqlalchemy import select
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import os

app = Flask(__name__)
csrf = CSRFProtect(app)

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
from restaurant_review.models import Review, Restaurant
db.create_all()
db.session.commit()

# initialize database migration management
migrate = Migrate(app, db)

@app.route('/', methods=['GET'])
def index():
    from restaurant_review.models import Restaurant
    print('Request for index page received')
    restaurants = Restaurant.query.all()
    #restaurants = Restaurant.annotate(avg_rating=func.avg('review__rating')).annotate(review_count=func.count('review'))
    #return render_template('index.html', restaurants=restaurants )
    return render_template('index.html')

@app.route('/<int:id>', methods=['GET'])
def details(id):
    from restaurant_review.models import Restaurant
    print('Request for restaurant details page received')
    restaurant = select(Restaurant).where(Restaurant.name==id)
    return render_template('details.html', restaurant=restaurant)

@app.route('/create', methods=['GET'])
def create_restaurant():
    print('Request for add restaurant page received')
    return render_template('create_restaurant.html')

@app.route('/add', methods=['POST'])
@csrf.exempt
def add_restaurant():
    from restaurant_review.models import Restaurant
    try:
        name = request.values.get('restaurant_name')
        street_address = request.values.get('street_address')
        description = request.values.get('description')
    except (KeyError):
        # Redisplay the question voting form.
        return render_template('add_restaurant.html', {
            'error_message': "You must include a restaurant name, address, and description",
        })
    else:
        restaurant = Restaurant()
        restaurant.name = name
        restaurant.street_address = street_address
        restaurant.description = description
        db.session.add(restaurant)
        db.session.commit()

        return redirect(url_for('details', id=restaurant.id))

@app.route('/review/<int:id>', methods=['POST'])
@csrf.exempt
def add_review(id):
    from restaurant_review.models import Restaurant, Review
    restaurant = select(Restaurant).where(Restaurant.id==id)
    try:
        user_name = request.values.get('user_name')
        rating = request.values.get('rating')
        review_text = request.values.get('review_text')
    except (KeyError):
        #Redisplay the question voting form.
        return render_template('add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        review = Review()
        review.restaurant = restaurant
        review.review_date = datetime.now()
        review.user_name = user_name
        review.rating = rating
        review.review_text = review_text
        Review.save(review)
                
    return redirect(url_for('details', id=id))        

@app.context_processor
def utility_processor():
    def star_rating(avg_rating, review_count):    
        stars_percent = round((avg_rating / 5.0) * 100) if review_count > 0 else 0
        return {'avg_rating': avg_rating, 'review_count': review_count, 'stars_percent': stars_percent}
    return dict(star_rating=star_rating)

if __name__ == '__main__':
   app.run()