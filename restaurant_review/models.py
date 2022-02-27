from restaurant_review.app import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, validates

# declarative base class
Base = declarative_base()

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    name = Column(String(50))
    street_address = Column(String(50))
    description = Column(String(250))
    def __str__(self):
        return self.name

class Review(db.Model):
    __tablename__ = 'review'
    restaurant = Column(String, ForeignKey('restaurant.name', ondelete="CASCADE"))
    user_name = Column(String(20))
    rating = Column(Integer)
    review_text = Column(String(500))
    review_date = Column(DateTime)

    @validates('rating')
    def validate_rating(self, key, value):
        assert value is None or (1 <= value <= 100)
        return value

    def __str__(self):
        return self.restaurant.name + " (" + self.review_date.strftime("%x") +")"