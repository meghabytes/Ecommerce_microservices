from flask import Flask, request, jsonify, render_template, redirect
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://mongodb-service:27017/")  # Connection to MongoDB
db = client["product_db"]
collection = db["products"]
cart_collection = db["cart"]  # Collection for user's cart
orders_collection = db["orders"]  # Collection for storing orders

# Global variable to hold the current userID
userID = None

@app.route('/products', methods=['GET'])
def get_products():
    global userID
    userID = request.args.get('userID')  # Get userID from query parameters
    print("UserID:", userID)

    products = []
    for product in collection.find():
        product["_id"] = str(product["_id"])  # Convert ObjectId to string
        products.append(product)
        print(product)
    return render_template('product.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = float(request.form.get('price'))  # Convert price to float
    description = request.form.get('description')

    product = {'Name': name, 'Price': price, 'Description': description}
    collection.insert_one(product)
    print(product)

    return jsonify({'message': 'Product added successfully!'})

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    global userID
    product_id = request.form.get('product_id')  # Get product_id from form data
    product_name = request.form.get('product_name')

    # Create entry for user's cart
    cart_entry = {'userID': userID, 'product_id': product_id, 'product_name': product_name}
    result = cart_collection.insert_one(cart_entry)

    if result.acknowledged:
        return jsonify({'message': f'Item "{product_name}" added to cart successfully!'}), 200

    return jsonify({'error': 'Failed to add item to cart!'}), 500

@app.route('/checkout', methods=['POST'])
def checkout():
    global userID
    print("Starting checkout process with userID:", userID)

    cart_items = list(cart_collection.find({'userID': userID}))
    if not cart_items:
        print("No items in the cart for userID:", userID)
        return jsonify({'error': 'Cart is empty!'}), 400

    total_price = 0
    for item in cart_items:
        product = collection.find_one({'_id': ObjectId(item['product_id'])})
        if product is None:
            print("Product not found for product_id:", item['product_id'])
            return jsonify({'error': 'Product not found!'}), 404
        price_str = product['Price'].replace('$', '').strip()  # Remove dollar sign and trim whitespace
        price = float(price_str)
        
        total_price += price


    # Additional logging to ensure the total_price calculation works
    print("Total price calculated:", total_price)

    order = {
        'userID': userID,
        'items': cart_items,
        'total_price': total_price,
        'status': 'Completed'
    }
    result = orders_collection.insert_one(order)
    
    if result.acknowledged:
        cart_collection.delete_many({'userID': userID})
        print("Order created with order_id:", result.inserted_id)
        return jsonify({
            'message': 'Checkout completed successfully!',
            'order_id': str(result.inserted_id),
            'total_price': total_price
        }), 200
    else:
        print("Failed to create order")
        return jsonify({'error': 'Checkout failed!'}), 500

@app.route('/order', methods=['POST', 'GET'])
def change_to_order():
    return redirect(f'http://localhost:5003/?userID={userID}')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
