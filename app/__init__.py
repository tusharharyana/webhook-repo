from flask import Flask

from app.webhook.routes import webhook
from .extensions import mongo


# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # MongoDB configuration
    app.config["MONGO_URI"] = "mongodb+srv://haryanatushar:UEKfsni52gJ3VXDz@cluster0.figgbyy.mongodb.net/github_webhooks?retryWrites=true&w=majority&appName=Cluster0"
    
    # Initialize Mongo with app    
    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
