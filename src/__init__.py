from flask import Flask
from src.auth import auth
from flask_cors import CORS
from src.transaction import transaction
from src.store import store
from src.profile import profile
from src.cart import cart
from src.payment import payment



def create_app():
    app = Flask(__name__)
    CORS(app=app)

    app.register_blueprint(cart)
    app.register_blueprint(profile)
    app.register_blueprint(store)
    app.register_blueprint(transaction)
    app.register_blueprint(auth)
    app.register_blueprint(payment)
    
    return app

    