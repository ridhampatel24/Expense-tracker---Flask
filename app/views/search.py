from flask import redirect, render_template, url_for, request, g
from app.models import Item, Category, Bank
from app import app
from flask_msearch import Search
from app.extensions import db

search = Search(app, db=db)
search.init_app(app)


def search(user):
    if not g.search_form.validate():
        return redirect(url_for("index"))

    # page = request.args.get('page', 1, type=int)
    # items, total = Item.search(
    #     g.search_form.q.data, page, app.config['POSTS_PER_PAGE'])
    # next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
    #     if total > page * app.config['POSTS_PER_PAGE'] else None
    # prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) \
    #     if page > 1 else None
    # print("Data: ", g.search_form.q.data, "Items: ", items, "\nTotal: ", total)

    items = (
        Item.query.msearch(
            g.search_form.q.data,
            fields=["name", "price", "payment_mode", "transaction_date"],
        )
        .filter_by(user_id=user.id)
        .all()
    )
    categories = (
        Category.query.msearch(g.search_form.q.data, fields=["name"])
        .filter_by(category_status=1, owner_id=user.id)
        .all()
    )
    banks = (
        Bank.query.msearch(g.search_form.q.data, fields=["name", "balance"])
        .filter_by(bank_status=1, owner_id=user.id)
        .all()
    )

    return render_template(
        "search.html",
        items=items,
        categories=categories,
        banks=banks,
        profile_photo=user.profile_photo,
        isAuthorize=True,
    )
