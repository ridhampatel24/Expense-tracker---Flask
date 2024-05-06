from flask import Blueprint
from app.utils.authenticate import token_required
from app.views import category as category_view

category_route = Blueprint("category_route", __name__)


@category_route.route("/category", methods=["GET", "POST"])
@token_required
def category(current_user):
    return category_view.category(current_user)


@category_route.route(
    "/category_details/edit/<int:categoryId>", methods=["GET", "POST"]
)
@token_required
def edit_category_details(user, categoryId):
    return category_view.edit_category_details(user, categoryId)


@category_route.route(
    "/category_details/delete/<int:categoryId>", methods=["GET", "POST"]
)
@token_required
def delete_category_details(user, categoryId):
    popup = {
        "msg": "Deleted category, although you can still restore it.",
        "category": "warning",
    }
    return category_view.change_category_status(
        user=user, categoryId=categoryId, status=2, popup=popup
    )


@category_route.route("/category_details/restore/<int:categoryId>")
@token_required
def restore_category_details(user, categoryId):
    popup = {"msg": "Restored category details.", "category": "success"}
    return category_view.change_category_status(
        user=user, categoryId=categoryId, status=1, popup=popup
    )


@category_route.route(
    "/category_details/filter/", methods=["GET", "POST"]
)
@token_required
def filter_items_by_category(user):
    return category_view.filter_items(user)


@category_route.route("/category_details/permanently_delete/<int:categoryId>")
@token_required
def parmanently_delete_category_details(user, categoryId):
    popup = {"msg": "Bank details deleted permanently.", "category": "warning"}
    return category_view.change_category_status(
        user=user, categoryId=categoryId, status=3, popup=popup
    )
