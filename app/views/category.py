from flask import redirect, render_template, url_for, flash
from app.forms import AddCategory, FilterForm
from app.extensions import db
from app.models import Category


def filter_items(user):
    category_form = AddCategory()
    filter_form = FilterForm()
    filter_form.submit.label.text = "Filter by category"
    if filter_form.validate_on_submit():
        filter_category = filter_form.filter_name.data
        category_id = None
        for category in user.category:
            if category.name.lower() == filter_category.lower() and category.category_status == 1:
                category_id = category.id
                break
        if not category_id:
            flash("Unauthorize access !", "danger")
            return redirect(url_for('category_route.category'))
        else:
            filter_form.submit.label.text = "Filter by category"
            categories_list = []
            for category in user.category:
                if category.category_status == 1:
                    categories_list.append((category.name, category.name))
            categories_list.sort()
            filter_form.filter_name.label.text = "Filter items by category"
            filter_form.filter_name.choices = categories_list.copy()
            category_details = Category().query.filter_by(id=category_id).first()
            filter_items_show = category_details.item
            return render_template(
                "category.html",
                profile_photo=user.profile_photo,
                isAuthorize=True,
                form=category_form,
                filter_form=filter_form,
                user=user,
                filter_items=filter_items_show
            )
    return redirect(url_for('category_route.category'))


def category(user):
    category_form = AddCategory()
    filter_form = FilterForm()
    if category_form.validate_on_submit():
        add_category = Category(name=category_form.name.data, owner_id=user.id)
        db.session.add(add_category)
        db.session.commit()
        flash("Category Added successfully...", "success")
        return redirect(url_for("category_route.category"))
    filter_form.submit.label.text = "Filter by category"
    categories_list = []
    for category in user.category:
        if category.category_status == 1:
            categories_list.append((category.name, category.name))
    categories_list.sort()
    filter_form.filter_name.label.text = "Filter items by category"
    filter_form.filter_name.choices = categories_list.copy()
    return render_template(
        "category.html",
        profile_photo=user.profile_photo,
        isAuthorize=True,
        form=category_form,
        filter_form=filter_form,
        user=user,
    )


def edit_category_details(user, categoryId):
    have_access = False
    category_form = AddCategory()
    category_form.submit.label.text = "Update Details"
    if category_form.validate_on_submit():
        isUpdate = False
        for category in user.category:
            if category.id == categoryId:
                category.name = category_form.name.data
                isUpdate = True
        if not isUpdate:
            flash("Unauthorize access !", "danger")
            return redirect(url_for("category_route.category"))
        db.session.commit()
        flash("category label updated successfully.", "success")
        return redirect(url_for("category_route.category"))
    for category in user.category:
        if category.id == categoryId:
            have_access = True
            category_form.name.data = category.name
    if not have_access:
        flash("Unauthorize access !", "danger")
        return redirect(url_for("category_route.category"))
    filter_form = FilterForm()
    filter_form.submit.label.text = "Filter by category"
    categories_list = []
    for category in user.category:
        if category.category_status == 1:
            categories_list.append((category.name, category.name))
    categories_list.sort()
    filter_form.filter_name.label.text = "Filter items by category"
    filter_form.filter_name.choices = categories_list.copy()
    return render_template(
        "category.html",
        user=user,
        categoryId=categoryId,
        form=category_form,
        filter_form=filter_form,
        profile_photo=user.profile_photo,
        isAuthorize=True,
    )


def change_category_status(user, categoryId, status, popup):
    have_access = False
    for category in user.category:
        if category.id == categoryId:
            have_access = True
            category.category_status = status
            if status == 2:
                user.deleted_category += 1
            else:
                user.deleted_category -= 1
            break
    if not have_access:
        flash("Unauthorize access !", "danger")
        return redirect(url_for("category_route.category"))
    db.session.commit()
    flash(popup["msg"], popup["category"])
    return redirect(url_for("category_route.category"))
