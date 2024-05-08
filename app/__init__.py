from flask import Flask, render_template, g
from flask_session import Session
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static",
    static_url_path="/",
)

from app.config import Config

app.config.from_object(Config)

# from elasticsearch import Elasticsearch

# app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
#     if app.config['ELASTICSEARCH_URL'] else None

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)

from app.extensions.db import db

from app import models

with app.app_context():
    db.create_all()

from app import forms

from app.routes import auth_route, bank_route, category_route, item_route

app.register_blueprint(auth_route)
app.register_blueprint(bank_route)
app.register_blueprint(category_route)
app.register_blueprint(item_route)

from app.forms.search_form import SearchForm


@app.before_request
def before_request():
    g.search_form = SearchForm()


@app.errorhandler(404)
def error(e):
    return render_template("404.html")
