from flask import Flask
from app.webhook.routes import webhook
from .extensions import mongo
from app.api.routes import api
from flask_cors import CORS

# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # MongoDB configuration
    app.config["MONGO_URI"] = "mongodb+srv://haryanatushar:UEKfsni52gJ3VXDz@cluster0.figgbyy.mongodb.net/github_webhooks?retryWrites=true&w=majority&appName=Cluster0"
    
    # Allow cross-origin requests 
    CORS(app)
    
    # Initialize Mongo with app    
    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(api)

    return app
