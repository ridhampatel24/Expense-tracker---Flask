from flask import redirect, url_for, render_template, flash
from app.forms import AddBank, FilterForm
from app.extensions import db
from app.models import Bank


def filter_items_by_bank(user):
    bank_form = AddBank()
    filter_form = FilterForm()
    if filter_form.validate_on_submit():
        filter_bank = filter_form.filter_name.data
        bank_id = None
        for bank in user.bank:
            if bank.name.lower() == filter_bank.lower() and bank.bank_status == 1:
                bank_id = bank.id
                break
        if not bank_id:
            flash("Unauthorize access !", "danger")
            return redirect(url_for('bank_route.bank'))
        else:
            filter_form.submit.label.text = "Filter by bank"
            banks_list = []
            for bank in user.bank:
                if bank.bank_status == 1:
                    banks_list.append((bank.name, bank.name))
            banks_list.sort()
            filter_form.submit.label.text = "Filter by Bank"
            filter_form.filter_name.label.text = "Filter items by bank"
            filter_form.filter_name.choices = banks_list.copy()
            bank_details = Bank().query.filter_by(id=bank_id).first()
            filter_items_show = bank_details.item
            return render_template(
                "bank.html",
                profile_photo=user.profile_photo,
                isAuthorize=True,
                form=bank_form,
                filter_form=filter_form,
                user=user,
                filter_items=filter_items_show
            )
    return redirect(url_for('bank_route.bank'))


def bank(user):
    bank_form = AddBank()
    filter_form = FilterForm()
    if bank_form.validate_on_submit():
        add_bank = Bank(
            name=bank_form.name.data, balance=bank_form.balance.data, owner_id=user.id
        )
        db.session.add(add_bank)
        db.session.commit()
        flash("Bank details added successfully...", "success")
        return redirect(url_for("bank_route.bank"))
    banks = user.bank
    filter_form.submit.label.text = "Filter by bank"
    banks_list = []
    for bank in banks:
        if bank.bank_status == 1:
            banks_list.append((bank.name, bank.name))
    banks_list.sort()
    filter_form.filter_name.label.text = "Filter items by bank"
    filter_form.filter_name.choices = banks_list.copy()
    return render_template(
        "bank.html",
        profile_photo=user.profile_photo,
        isAuthorize=True,
        form=bank_form,
        user=user,
        filter_form=filter_form
    )


def edit_bank_details(user, bankId):
    have_access = False
    bank_form = AddBank()
    bank_form.submit.label.text = "Update Details"
    filter_form = FilterForm()
    filter_form.submit.label.text = "Filter by bank"
    banks_list = []
    if bank_form.validate_on_submit():
        isUpdate = False
        for bank in user.bank:
            if bank.id == bankId:
                bank.name = bank_form.name.data
                bank.balance = bank_form.balance.data
                isUpdate = True
        if not isUpdate:
            flash("Unauthorize access !", "danger")
            return redirect(url_for("bank_route.ebank"))
        db.session.commit()
        flash("Bank details updated successfully.", "success")
        return redirect(url_for("bank_route.bank"))
    for bank in user.bank:
        if bank.id == bankId:
            have_access = True
            bank_form.name.data = bank.name
            bank_form.balance.data = bank.balance
        if bank.bank_status == 1:
            banks_list.append((bank.name, bank.name))
    banks_list.sort()
    filter_form.filter_name.label.text = "Filter items by bank"
    filter_form.filter_name.choices = banks_list.copy()
    if not have_access:
        flash("Unauthorize access !", "danger")
        return redirect(url_for("bank_route.bank"))
    return render_template(
        "bank.html",
        user=user,
        bankId=bankId,
        form=bank_form,
        profile_photo=user.profile_photo,
        isAuthorize=True,
        filter_form=filter_form
    )


def change_bank_status(user, bankId, status, popup):
    have_access = False
    for bank in user.bank:
        if bank.id == bankId:
            have_access = True
            bank.bank_status = status
            if status == 2:
                user.deleted_bank += 1
            else:
                user.deleted_bank -= 1
    if not have_access:
        flash("Unauthorize access !", "danger")
        return redirect(url_for("bank_route.bank"))
    db.session.commit()
    flash(popup["msg"], popup["category"])
    return redirect(url_for("bank_route.bank"))
