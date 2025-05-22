from app.extensions import db
from datetime import datetime

class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    product_id =db.Column(db.Integer, db.ForeignKey("products.id"))
    items = db.Column(db.JSON, nullable=False)  # List of item dicts
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="processing")
    created_at = db.Column(db.DateTime, default=datetime.now())

def __init__ (self, items, product_id, user_id, total_amount):
    super(Order, self).__init__()
    self.items = items
    self.product_id = product_id
    self.user_id = user_id
    self.total_amount = total_amount

def order_info(self):
       return  f" {self.items} {self.amount}"