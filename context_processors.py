from .blueprints.product.models import  Product
from flask_login import current_user
from flask import current_app as app, session

@app.context_processor
def get_product_categories():
    return { 'product_categories': [c for c in Category.query.order_by(Category.name).all()] }



