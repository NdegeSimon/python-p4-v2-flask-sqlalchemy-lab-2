from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)

    reviews = relationship("Review", back_populates="customer", cascade="all, delete-orphan")
    items = association_proxy("reviews", "item")

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Customer must have a name")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "reviews": [review.to_dict() for review in self.reviews],
        }


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)

    reviews = relationship("Review", back_populates="item", cascade="all, delete-orphan")
    customers = association_proxy("reviews", "customer")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "reviews": [review.to_dict() for review in self.reviews],
        }


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)

    customer = relationship("Customer", back_populates="reviews")
    item = relationship("Item", back_populates="reviews")

    def to_dict(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "customer": {
                "id": self.customer.id,
                "name": self.customer.name,
            } if self.customer else None,
            "item": {
                "id": self.item.id,
                "name": self.item.name,
                "price": self.item.price,
            } if self.item else None,
        }
