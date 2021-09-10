from market import app
from flask import render_template, redirect, url_for, flash, request
from market.model import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user, login_manager

login_manager.login_view = "login_page"


@app.route('/')
@app.route('/home')
def home_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    items = Item.query.filter_by(owner=None)

    # return render_template('home.html')
    return render_template('home.html', items=items, purchase_form=purchase_form, selling_form=selling_form)


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    return render_template('index.html')


@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    items = Item.query.filter_by(owner=None)
    return render_template('cart.html', items=items, purchase_form=purchase_form, selling_form=selling_form)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    items = Item.query.filter_by(owner=None)
    return render_template('checkout.html', items=items, purchase_form=purchase_form, selling_form=selling_form)


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        # Purchase Item Logic
        purchase_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchase_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulations! you Purchased {p_item_object.name} for ₦{p_item_object.price}',
                      category="success")
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category="danger")
        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Congratulations! you Sold {s_item_object.name} Back to market for ₦{s_item_object.price}',
                      category="success")
            else:
                flash(f"Unfortunately, Something Went Wrong with Sell {s_item_object.name}", category="danger")

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,
                               selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(full_name=form.full_name.data,
                              username=form.username.data,
                              email_address=form.email_address.data,
                              gender=form.gender.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account Created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:  # if No Errors from Validation
        for err_msg in form.errors.values():
            flash(f'there was an Error Creating a user{err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            user_type = attempted_user.user_type

            if user_type == "1":
                flash(f'Hello Admin! You logged in as {attempted_user.username}', category='success')
                return redirect(url_for('admin_page'))
            else:
                flash(f'Howdy {attempted_user.username}! Welcome to Moses\' Store ', category='success')
                return redirect(url_for('market_page'))
        else:
            flash('Username or password does not match! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You've Been Logged out!", category='info')
    return redirect(url_for("home_page"))
