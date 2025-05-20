from flask import Flask
from app.extensions import db,migrate


#application factory function
def create_app():
    
    #app instance
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app,db)



    @app.route("/")
    def home():
        return "Python Exam"
    
  
    
    

    return app

