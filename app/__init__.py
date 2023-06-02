from flask import Flask

app = Flask(__name__)

#import all the routes for the routes.py file 

from app import routes