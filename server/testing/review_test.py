from app import app, db
from server.models import Customer, Item, Review


class TestReview:
    """Tests for the Review model in models.py"""

    def test_can_be_instantiated(self):
        """Review can be invoked to create a Python object."""
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        """Review can be instantiated with a comment attribute."""
        r = Review(comment="great product!")
        assert r.comment == "great product!"

    def test_can_be_saved_to_database(self):
        """Review can be added to a transaction and committed to the review table with comment column."""
        with app.app_context():
            assert "comment" in Review.__table__.columns

            c = Customer(name="Phil")
            i = Item(name="Insulated Mug", price=9.99)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment="great!", customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            assert hasattr(r, "id")
            assert db.session.query(Review).filter_by(id=r.id).first()

    def test_is_related_to_customer_and_item(self):
        """Review has foreign keys and relationships to Customer and Item."""
        with app.app_context():
            assert "customer_id" in Review.__table__.columns
            assert "item_id" in Review.__table__.columns

            c = Customer(name="Alice")
            i = Item(name="Coffee Mug", price=5.99)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment="awesome mug!", customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # check foreign keys
            assert r.customer_id == c.id
            assert r.item_id == i.id

            # check relationships
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews
