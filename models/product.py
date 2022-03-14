from datetime import datetime
from main import db

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    buying_price = db.Column(db.Integer, nullable=False, default=0)
    selling_price = db.Column(db.Integer, nullable=False, default=0)
    profit = db.Column(db.Integer, nullable=False, default=0)
    percentage_profit = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.String(100), default=datetime.now())


    # update record
    @classmethod
    def update_by_id(cls,id, product_name=None,  quantity=0, selling_price=0, buying_price=0, profit=0, percentage_profit=0):
        record = cls.query.filter_by(id=id).first()

        if record:

            record.product_name = product_name
            record.quantity = quantity
            record.buying_price = buying_price
            record.selling_price = selling_price
            record.profit = profit
            record.percentage_profit = percentage_profit

            db.session.commit()
            return record
        return record


    # fetch records id
    @classmethod
    def delete_product(cls,id):
        delete_record = cls.query.filter_by(id=id)
        
        if delete_record.first():

            delete_record.delete()
            db.session.commit()
            return True
        else:
            return False

