from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb://mongodb-service:27017/")  # Connection to MongoDB
db = client["product_db"]
cart_collection = db["cart"]
collection = db["products"]
orders_collection = db["orders"]
@app.route('/cart', methods=['GET'])
def show_cart():
    userID = request.args.get('userID')
    if not userID:
        return "User ID is required", 400

    cart_items = list(cart_collection.find({'userID': userID}))

    total_price = 0
    for item in cart_items:
        # Convert ObjectId to string for easy rendering
        item["_id"] = str(item["_id"])
        
        # Get the product details to calculate the total price
        product = collection.find_one({'_id': ObjectId(item['product_id'])})
        if product:
            price_str = product['Price'].replace('$', '').strip()  # Remove dollar sign and trim whitespace
            price = float(price_str)
            total_price += price

    # Pass the total price to the template
    return render_template('cart.html', cart_items=cart_items, userID=userID, total_price=total_price)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    userID = request.form.get('userID')

    if not product_id or not userID:
        return "Product ID and User ID are required", 400

    result = cart_collection.delete_one({'userID': userID, 'product_id': product_id})

    if result.deleted_count > 0:
        return redirect(f'/cart?userID={userID}')  # Redirect back to the cart after removal
    else:
        return "Item not found in cart", 404
    
@app.route('/make_payment', methods=['POST'])
def make_payment():
    userID = request.form.get('userID')
    if not userID:
        return "User ID is required", 400

    # Simulate a redirect to a payment gateway
    # You can add additional logic here, like creating a payment order or logging payment details
    return f"Redirecting to PayPal for User {userID}. Please wait...", 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)  



