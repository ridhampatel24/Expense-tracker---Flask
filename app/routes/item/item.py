from flask import Blueprint, g, render_template
from app.utils.authenticate import token_required
from app.views import item, search as search_view

item_route = Blueprint("item_route", __name__)


@item_route.route("/home", methods=["GET", "POST"])
@token_required
def home(user):
    return item.home(user)


@item_route.route("/item_details/edit/<int:itemId>", methods=["GET", "POST"])
@token_required
def edit_item_details(user, itemId):
    return item.edit_item_details(user, itemId)


@item_route.route("/item_details/delete/<int:itemId>")
@token_required
def delete_item_details(user, itemId):
    return item.delete_item_details(user, itemId)


@item_route.route("/history/<int:page>")
@token_required
def history(user, page=0):
    return item.history(user, page)


@item_route.route("/search")
@token_required
def search(user):
    return search_view.search(user)
