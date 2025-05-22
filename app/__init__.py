from flask import Flask
from app.extensions import db,migrate, jwt
from flask_bcrypt import Bcrypt
from app.controllers.users.users_controller import users
from app.controllers.products.products_controller import products
from app.controllers.orders.orders_controller import orders
from app.controllers.auth.auth_controller import auth

# Initialize Bcrypt outside the create_app function
bcrypt = Bcrypt()



#application factory function
def create_app():
    
    #app instance
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
# Initialize extensions
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)

# Import the models
    from app.models.product import Product
    from app.models.user import User
    from app.models.order import Order
    
    

# Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(orders)
    app.register_blueprint(products)
    

    @app.route("/")
    def home():
        return "Python Exam"
    
  
    
    

    return app

