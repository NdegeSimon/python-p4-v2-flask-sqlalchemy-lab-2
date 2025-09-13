from app import app, db
from server.models import Customer, Item, Review


class TestSerialization:
    '''models in models.py'''

    def test_customer_is_serializable(self):
        '''customer is serializable'''
        with app.app_context():
            c = Customer(name='Phil')
            db.session.add(c)
            db.session.commit()

            r = Review(comment='great!', customer=c)
            db.session.add(r)
            db.session.commit()

            customer_dict = c.to_dict()

            assert customer_dict['id']
            assert customer_dict['name'] == 'Phil'
            assert customer_dict['reviews']
            # reviews should not recursively contain customer again
            assert 'customer' not in customer_dict['reviews']

    def test_item_is_serializable(self):
        '''item is serializable'''
        with app.app_context():
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add(i)
            db.session.commit()

            r = Review(comment='great!', item=i)
            db.session.add(r)
            db.session.commit()

            item_dict = i.to_dict()

            assert item_dict['id']
            assert item_dict['name'] == 'Insulated Mug'
            assert item_dict['price'] == 9.99
            assert item_dict['reviews']
            # reviews should not recursively contain item again
            assert 'item' not in item_dict['reviews']

    def test_review_is_serializable(self):
        '''review is serializable'''
        with app.app_context():
            c = Customer(name='Alice')
            i = Item(name='Coffee Maker', price=49.99)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            review_dict = r.to_dict()

            assert review_dict['id']
            assert review_dict['customer']
            assert review_dict['item']
            assert review_dict['comment'] == 'great!'
            # customer dict should not contain nested reviews
            assert 'reviews' not in review_dict['customer']
            # item dict should not contain nested reviews
            assert 'reviews' not in review_dict['item']
