from flask import Blueprint
from app.utils.authenticate import token_required
from app.views import bank as bank_view

bank_route = Blueprint("bank_route", __name__)


@bank_route.route("/bank", methods=["GET", "POST"])
@token_required
def bank(current_user):
    return bank_view.bank(current_user)


@bank_route.route("/bank_details/edit/<int:bankId>", methods=["GET", "POST"])
@token_required
def edit_bank_details(user, bankId):
    return bank_view.edit_bank_details(user, bankId)


@bank_route.route("/bank_details/delete/<int:bankId>", methods=["GET", "POST"])
@token_required
def delete_bank_details(user, bankId):
    popup = {
        "msg": "Deleted bank details, although you can still restore it.",
        "category": "warning",
    }
    return bank_view.change_bank_status(user=user, bankId=bankId, status=2, popup=popup)


@bank_route.route("/bank_details/filter", methods=["GET", "POST"])
@token_required
def filter_items_by_bank(user):
    return bank_view.filter_items_by_bank(user)


@bank_route.route("/bank_details/restore/<int:bankId>")
@token_required
def restore_bank_details(user, bankId):
    popup = {"msg": "Restored bank details.", "category": "success"}
    return bank_view.change_bank_status(user=user, bankId=bankId, status=1, popup=popup)


@bank_route.route("/bank_details/parmanently_delete/<int:bankId>")
@token_required
def parmanently_delete_bank_details(user, bankId):
    popup = {"msg": "Bank details deleted permanently.", "category": "warning"}
    return bank_view.change_bank_status(user=user, bankId=bankId, status=3, popup=popup)
