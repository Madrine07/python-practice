from app.extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    product_name = db.Column(db.String(40))
    description = db.Column(db.String(200), nullable = False)
    image = db.Column(db.String(100), nullable = True) 
    created_at = db.Column(db.DateTime, default= datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())

def __init__ (self, product_name,description, image=None):
          super(Product, self).__init__()
                         
          self.product_name = product_name   
          self.description = description           
          self.image= image
          
         
        

def product_info(self):
       return  f" {self.product_name} {self.description}"