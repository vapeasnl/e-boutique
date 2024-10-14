from flask import Flask, render_template, request, redirect, url_for
from models import db, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e-boutique.db'
db.init_app(app)

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
@app.route('/product/<int:product_id>/reviews', methods=['GET', 'POST'])
def product_reviews(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':
        review = request.form['review']
        # Save review to the database
    reviews = []  # Fetch reviews from the database
    return render_template('product_reviews.html', product=product, reviews=reviews)

@app.route('/search')
def search():
    query = request.args.get('q')
    results = Product.query.filter(Product.name.contains(query)).all()
    return render_template('search_results.html', results=results)

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
