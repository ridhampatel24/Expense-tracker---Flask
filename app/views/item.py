from flask import redirect, render_template, url_for, flash, request
from app.forms import AddItem
from app.extensions import db
from app.models import Category, Item
from app import app


def home(user):
    item_form = AddItem()
    categories_list = []
    banks_list = []
    if len(user.category) == 0:
        add_category = Category(name="other")
        user.category.append(add_category)
        db.session.commit()
        categories_list.append(("other", "Other"))
    else:
        for category in user.category:
            if category.category_status == 1:
                categories_list.append((category.name, category.name))
    if user.bank:
        for bank in user.bank:
            if bank.bank_status == 1:
                banks_list.append((bank.name, bank.name))
    if item_form.validate_on_submit():
        item_name = item_form.name.data
        item_price = item_form.price.data
        item_category = item_form.category_name.data
        item_payment = item_form.payment_mode.data
        item_bank = item_form.bank_name.data or ""
        category_id = None
        bank_id = None
        if item_payment.lower() != "cash" and user.bank:
            for bank in user.bank:
                if item_bank.lower() == bank.name.lower() and bank.bank_status == 1:
                    bank_id = bank.id
                    bank.balance -= float(item_price)
                    break
        if item_payment.lower() != "cash" and bank_id is None:
            item_payment = "cash"
        if user.category:
            for category in user.category:
                if ( 
                    item_category.lower() == category.name.lower() 
                    and category.category_status == 1
                ):
                    category_id = category.id
                    break
        new_item = Item(
            name=item_name,
            price=item_price,
            payment_mode=item_payment,
            category_id=category_id,
            bank_id=bank_id,
            user_id=user.id,
        )
        db.session.add(new_item)
        db.session.commit()
        flash("Item added to database.", "success")
        return redirect(url_for("item_route.home"))

    categories_list.sort()
    banks_list.sort()
    if len(banks_list) == 0:
        item_form.payment_mode.choices = [("cash", "Cash")]
    item_form.category_name.choices = categories_list.copy()
    item_form.bank_name.choices = banks_list.copy()

    return render_template(
        "home.html",
        user=user,
        profile_photo=user.profile_photo,
        isAuthorize=True,
        form=item_form,
    )


def edit_item_details(user, itemId):
    have_access = False
    item_form = AddItem()
    categories_list = []
    banks_list = []
    item_form.submit.label.text = "Update Details"
    if item_form.validate_on_submit():
        is_update = False
        for item in user.item:
            if item.id == itemId:
                item.name = item_form.name.data
                old_price = item.price
                item.price = item_form.price.data
                old_payment_mode = item.payment_mode
                item.payment_mode = item_form.payment_mode.data
                item_category = item_form.category_name.data
                item_bank = item_form.bank_name.data or ""
                if old_payment_mode.lower() == "upi":
                    for bank in user.bank:
                        if bank.id == item.bank_id:
                            bank.balance += float(old_price)
                            break
                if item.payment_mode.lower() != "cash" and user.bank:
                    found_entry = False
                    for bank in user.bank:
                        if (
                            item_bank.lower() == bank.name.lower()
                            and bank.bank_status == 1
                        ):
                            item.bank_id = bank.id
                            bank.balance -= float(item_form.price.data)
                            found_entry = True
                            break
                    if not found_entry:
                        item.bank_id = None
                if item.payment_mode.lower() == "cash":
                    item.bank_id = None
                if item.payment_mode.lower() != "cash" and item.bank_id is None:
                    item.payment_mode = "cash"
                if user.category:
                    for category in user.category:
                        if (
                            item_category.lower() == category.name.lower()
                            and category.category_status == 1
                        ):
                            item.category_id = category.id
                            break
                is_update = True
                break
        if not is_update:
            flash("Unauthorize access !", "danger")
            return redirect(url_for("item_route.item"))
        db.session.commit()
        flash("Item details updated successfully.", "success")
        return redirect(url_for("item_route.home"))
    if user.category:
        for category in user.category:
            if category.category_status == 1:
                categories_list.append((category.name, category.name))
    if user.bank:
        for bank in user.bank:
            if bank.bank_status == 1:
                banks_list.append((bank.name, bank.name))

    categories_list.sort()
    banks_list.sort()

    for item in user.item:
        if item.id == itemId:
            have_access = True
            item_form.name.data = item.name
            item_form.price.data = item.price
            for category in user.category:
                if category.id == item.category_id:
                    item_form.category_name.data = category.name
                    break
            if item.payment_mode == "cash":
                item_form.payment_mode.data = "cash"
                item_form.bank_name.data = "no_bank"
            else:
                item_form.payment_mode.data = "upi"
                for bank in user.bank:
                    if bank.id == item.bank_id:
                        item_form.bank_name.data = bank.name
                        break
            break
    if not have_access:
        flash("Unauthorize access !", "danger")
        return redirect(url_for("item_route.home"))

    if len(banks_list) == 0:
        item_form.payment_mode.choices = [("cash", "Cash")]
    item_form.category_name.choices = categories_list.copy()
    item_form.bank_name.choices = banks_list.copy()
    return render_template(
        "home.html",
        user=user,
        itemId=itemId,
        form=item_form,
        profile_photo=user.profile_photo,
        isAuthorize=True,
    )


def delete_item_details(user, itemId):
    delete_item = Item.query.filter_by(id=itemId, user_id=user.id).first()
    if delete_item:
        if delete_item.payment_mode != "cash":
            for bank in user.bank:
                if bank.id == delete_item.bank_id:
                    bank.balance += float(delete_item.price)
                    break
        db.session.delete(delete_item)
        flash("Item deleted.", "warning")
        db.session.commit()
    else:
        flash("Unauthorize access!", "danger")
    return redirect(url_for("item_route.home"))


def history(user, page=0):
    items_total = len(user.item)
    skip_items = app.config["PER_PAGE_ITEM_VIEW"] * page
    remaining_items = items_total - skip_items
    if remaining_items < 0:
        flash("You can't exceed limit !", "warning")
        return redirect(url_for("item_route.history", page=0))
    pagination = {
        "offset": app.config["PER_PAGE_ITEM_VIEW"],
        "prev_btn_show": True,
        "next_btn_show": True,
    }
    if page == 0:
        pagination["prev_btn_show"] = False
    if remaining_items > app.config["PER_PAGE_ITEM_VIEW"]:
        items = (
            Item.query.filter_by(user_id=user.id)
            .limit(app.config["PER_PAGE_ITEM_VIEW"])
            .offset(skip_items)
        )
    else:
        pagination["next_btn_show"] = False
        items = (
            Item.query.filter_by(user_id=user.id)
            .limit(remaining_items)
            .offset(skip_items)
        )
    return render_template(
        "history.html",
        items=items,
        page=page,
        pagination=pagination,
        profile_photo=user.profile_photo,
        isAuthorize=True,
    )
