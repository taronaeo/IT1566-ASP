import shelve
from .. import UPLOAD_DIR, DB_USER_LOCATION, DB_PRODUCTS_LOCATION
from ..models import Product
from ..utils import check_filename

from werkzeug.utils import secure_filename
from flask import Blueprint, abort, flash, url_for, request, redirect, render_template
from flask_login import current_user, login_required

products = Blueprint('products', __name__)

#! Products
@products.route('/products')
def all_products():
  with shelve.open(DB_PRODUCTS_LOCATION) as db_products:
    return render_template('/products/products.html', user=current_user, db_products = db_products)

@products.route('/products/<uid>')
def view_product(uid: str):
  with shelve.open(DB_USER_LOCATION) as db_user, \
          shelve.open(DB_PRODUCTS_LOCATION) as db_products:

    if uid not in db_products:
      abort(404)
    
    return render_template('/products/view_product.html',
                           user=current_user, db_products = db_products, current_product = db_products[uid])
@products.route('/products/create_product', methods=['GET', 'POST'])
def create_product():
  if request.method == 'POST':
    name = request.form.get('name')
    product_img = request.files.get('product_img')
    description = request.form.get('description')
    category = request.form.get('category')
    price = request.form.get('price')

    if not name or \
            not product_img or \
            not description or \
            not category or \
            not price:
      flash('All fields must not be empty')
      return redirect(request.url)

    if not 6 <= len(name) <= 60:
      flash('Title must be within 6 to 60 characters long')
      return redirect(request.url)


    if not check_filename(product_img.filename):
      flash('Invalid file type. Only PNG and JPG files are accepted')
      return redirect(request.url)

    try:
      price = float(price)
    except ValueError:
      flash('Invalid price. It should be in decimal format')
      return redirect(request.url)

    filename = secure_filename(product_img.filename)  # type: ignore
    product_img.save(f'{UPLOAD_DIR}/{filename}')

    Product.create(
        name,  # type: ignore
        filename,
        description,
        price,
        category
    )
    return redirect(url_for('products.all_products'))

  return render_template('/products/create_product.html',
                         user=current_user)
  
@products.route('/products/<uid>/update', methods=['GET', 'POST'])
@login_required
def update_product(uid: str):
  with shelve.open(DB_PRODUCTS_LOCATION) as db_products:
    if request.method == 'POST':
      name = request.form.get('name')
      product_img = request.files.get('product_img')
      description = request.form.get('description')
      category = request.form.get('category')
      price = request.form.get('price')

      if not name or \
              not product_img or \
              not description or \
              not category or \
              not price:
        flash('All fields must not be empty')
        return redirect(request.url)

      if not 6 <= len(name) <= 60:
        flash('Title must be within 6 to 60 characters long')
        return redirect(request.url)


      if not check_filename(product_img.filename):
        flash('Invalid file type. Only PNG and JPG files are accepted')
        return redirect(request.url)

      try:
        price = float(price)
      except ValueError:
        flash('Invalid price. It should be in decimal format')
        return redirect(request.url)

      filename = secure_filename(product_img.filename)  # type: ignore
      product_img.save(f'{UPLOAD_DIR}/{filename}')

      Product.create(
          name,  # type: ignore
          filename,
          description,
          price,
          category
      )
      return redirect(url_for('products.all_products'))

    return render_template('/products/create_product.html',
                          user=current_user,
                          product = db_products[uid])

@products.route('/products/<uid>/delete')
def delete_product(uid: str):
  with shelve.open(DB_PRODUCTS_LOCATION) as db_products:
    if uid not in db_products:
      abort(404)

    del db_products[uid]
    flash('Product successfully deleted')

  return redirect(url_for('products.all_products'))

@products.route('/products/filter/<category>')
def filter_product(category:str):
  with shelve.open(DB_PRODUCTS_LOCATION) as db_products:
    products = []
    current_category = None
    for product in db_products.values():
      if product.category == category:
        products.append(product)
        current_category = category
    return render_template('/products/filter_products.html', user = current_user, products = products, category = current_category)