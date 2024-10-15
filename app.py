from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Product, User
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e-boutique.db'
app.secret_key = 'secrets.token_hex(16)'
db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and/or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='sha256')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/product/<int:product_id>/variations')
def product_variations(product_id):
    product = Product.query.get(product_id)
    variations = ProductVariation.query.filter_by(product_id=product_id).all()
    return render_template('product_variations.html', product=product, variations=variations)

@app.route('/advanced_search')
def advanced_search():
    brand = request.args.get('brand')
    rating = request.args.get('rating')
    discount = request.args.get('discount')
    # ... add more filters
    query = Product.query
    if brand:
        query = query.filter(Product.brand == brand)
    if rating:
        query = query.filter(Product.rating >= rating)
    if discount:
        query = query.filter(Product.discount >= discount)
    products = query.all()
    return render_template('search_results.html', products=products)

@app.route('/compare')
def compare():
    product_ids = request.args.getlist('product_ids')
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    return render_template('compare.html', products=products)

@app.route('/share_wishlist')
def share_wishlist():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
    products = [Product.query.get(item.product_id) for item in wishlist_items]
    # Logic to share wishlist
    return render_template('share_wishlist.html', products=products)

@app.route('/price_drop_notifications')
def price_drop_notifications():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return render_template('price_drop_notifications.html', notifications=notifications)

@app.route('/product/<int:product_id>/reviews', methods=['GET', 'POST'])

@app.route('/product/<int:product_id>/reviews', methods=['GET', 'POST'])
def product_reviews(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':
        rating = request.form.get('rating')
        review_text = request.form.get('review')
        if rating and review_text:
            new_review = Review(product_id=product_id, user_id=session.get('user_id'), rating=rating, review_text=review_text)
            db.session.add(new_review)
            db.session.commit()
        else:
            review = request.form.get('review')
            if review:
                # Save review to the database (implement the logic here)
                pass
    reviews = Review.query.filter_by(product_id=product_id).all()
    return render_template('product_reviews.html', product=product, reviews=reviews)

@app.route('/recommendations/<int:product_id>')
def recommendations(product_id):
    product = Product.query.get(product_id)
    recommendations = Recommendation.query.filter_by(product_id=product_id).all()
    recommended_products = [Product.query.get(rec.recommended_product_id) for rec in recommendations]
    return render_template('recommendations.html', product=product, recommended_products=recommended_products)


@app.route('/wishlist')
def wishlist():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
    products = [Product.query.get(item.product_id) for item in wishlist_items]
    return render_template('wishlist.html', products=products)

@app.route('/add_to_wishlist/<int:product_id>')
def add_to_wishlist(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    new_wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
    db.session.add(new_wishlist_item)
    db.session.commit()
    return redirect(url_for('wishlist'))

@app.route('/notifications')
def notifications():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return render_template('notifications.html', notifications=notifications)

def send_notification(user_id, message):
    new_notification = Notification(user_id=user_id, message=message)
    db.session.add(new_notification)
    db.session.commit()

# Example usage
# send_notification(user_id, "Your order status has changed.")

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/admin/products')
def admin_products():
    products = Product.query.all()
    return render_template('admin_products.html', products=products)

@app.route('/admin/dashboard')
def admin_dashboard():
    # Sample data for demonstration
    sales_data = {
        'total_sales': 5000,
        'total_orders': 150,
        'top_products': ['Product A', 'Product B', 'Product C']
    }
    return render_template('admin_dashboard.html', sales_data=sales_data)

@app.route('/filter')
def filter_products():
    name = request.args.get('name')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    availability = request.args.get('availability')

    query = Product.query
    if name:
        query = query.filter(Product.name.contains(name))
    if min_price:
        query = query.filter(Product.price >= float(min_price))
    if max_price:
        query = query.filter(Product.price <= float(max_price))
    if availability:
        query = query.filter(Product.is_available == (availability == 'true'))

    products = query.all()
    return render_template('filter_results.html', products=products)

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('category_products.html', category=category, products=products)



@app.route('/client/orders')
def client_orders():
    user_id = 1  # Replace with actual user ID from session
    orders = Order.query.filter_by(user_id=user_id).all()
    return render_template('client_orders.html', orders=orders)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']
        new_product = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin_products'))
    return render_template('add_product.html')

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('admin_products'))

@app.route('/client')
def client():
    # Fetch the logged-in user's orders
    user_id = 1  # This should be dynamically fetched from session or authentication method
    orders = Order.query.filter_by(user_id=user_id).all()
    return render_template('client.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)
