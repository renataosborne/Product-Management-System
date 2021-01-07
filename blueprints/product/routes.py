from app import db
from .import bp as shop
from flask import render_template, redirect, url_for, request, flash, session, jsonify, current_app as app
from .models import Product, ProductCategory
from app.blueprints.authentication.models import User
from flask_login import login_required, current_user
from datetime import datetime as dt


@product.route('/', methods=['GET'])
@login_required
def index():
    context = {
        'products': Product.query.all()
    }
    return render_template('/index.html', **context)




@product.route('/product', methods=['GET'])
@login_required
def single():
    product_id = request.args.get('id')

    context = {
        'p': Product.query.filter_by(name=product_id).first()
    }
    return render_template('product/single.html', **context)





@shop.route('/category', methods=['GET'])
@login_required
def category():
    category = request.args.get('name').title()

    context = {
        'category': Category.query.filter_by(name=category).first(),
        'products': Product.query.filter_by(category_id=Category.query.filter_by(name=category).first().id).all()
    }
    return render_template('product/index.html', **context)