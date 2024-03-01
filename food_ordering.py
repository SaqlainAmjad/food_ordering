from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/food_ordering'
db = SQLAlchemy(app)
# Tables for flask applications
# User tables
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100),unique=False, nullable=False)
    user_email = db.Column(db.String(120),unique=False, nullable=False)
    user_password = db.Column(db.String(20),unique=False, nullable=False)
    user_address = db.Column(db.String(100),unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    with app.app_context():
     db.create_all() 
# Menu tables
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True)

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    items = db.relationship('MenuItem', backref='subcategory', lazy=True)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)

class Add_To_Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable = False)
    quantity = db.Column(db.Integer,nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime,default=datetime.utcnow)

# Functions used in flask applications
def is_valid_email(email):
    # Regular expression for validating email addresses
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email) is None
def is_valid_password(password):
    symbol_count = len(re.findall(r'[!@#$%^&*()_+={}\[\]:;\"\'<>,.?/|\\~`-]', password))
    digit_count = len(re.findall(r'\d', password))
    if len(password) < 6:
        return False
    if symbol_count < 2:
        return False
    elif digit_count < 2:
        return False
    else:
        return True

# Routes in flask applications
@app.route('/app/sign_up',methods=['POST'])
def sign_up():
    data = request.get_json()
    user_name = data.get("user_name")
    user_email  = data.get("user_email")
    user_password = data.get("user_password")
    user_address = data.get("user_address")
    if user_name is None:
        return jsonify({"message":"Please enter user_name"})
    if user_email is None:
        return jsonify({"message":"Please enter email"})
    if user_password is None:
        return jsonify({"message":"Please enter your password"})
    if user_address is None:
        return jsonify({"message":"Please enter your valid address"})
    # to chech email is duplicate or not
    existing_user =User.query.filter(User.user_email==user_email).first()
    if existing_user:
        return jsonify({"message":"This email is already used. Please try another email."}),400
    # To check email is in correct format
    if is_valid_email(user_email):
        return jsonify({"message":"Please enter email in correct format:"})
    # To check is it a secure password
    if is_valid_password(user_password) == False:
       return jsonify({"message":"the password should be 6 characters long with atleast 2 symbols and 2 digits"})
    new_user = User(user_name=user_name,user_email=user_email,user_password=user_password,user_address=user_address)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"Succesfull Completed"}),200
@app.route('/app/login',methods=['POST'])
def login():
    data = request.get_json()
    user_email = data.get("user_email")
    user_password = data.get("user_password")
    email_found = User.query.filter(User.user_email==user_email).first()
    if email_found is None:
        return jsonify({"message":"Plaease enter a valid email"})
    if email_found.user_password != user_password:
        return jsonify({"message": "please enter correct password"})
    else:
        return jsonify({"message":"login successfully"})
@app.route("/categories",methods=['GET'])
def get_categories():
    categories = Category.query.with_entities(Category.name).all()
    available_categories = [{'name': category.name} for category in categories]
    return jsonify({"categories":available_categories})
@app.route('/subcategories', methods=['POST'])
def get_subcategories():
    data = request.get_json()
    category_name = data.get('category_name')

    if category_name:
        category = Category.query.filter_by(name=category_name).first()
        if category:
            subcategories = [sub.name for sub in category.subcategories]
            return jsonify({'subcategories': subcategories})
        else:
            return jsonify({'message': 'Category not found'}), 404
    else:
        return jsonify({'message': 'Category name not provided'}), 400

# Route to retrieve menu items for a given subcategory
@app.route('/items', methods=['POST'])
def get_items_by_subcategory():
    data = request.get_json()
    subcategory_name = data.get('subcategory_name')

    if subcategory_name:
        subcategory = Subcategory.query.filter_by(name=subcategory_name).first()
        if subcategory:
            items = [[sub.name , sub.price] for sub in subcategory.items]
            return jsonify({'subcategories': items})
        else:
            return jsonify({'message': 'Subcategory not found'}), 404
    else:
        return jsonify({'message': 'Subcategory name not provided'}), 400
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get("product_id")
    user_id = data.get("user_id")
    quantity = data.get("quantity")
    name = data.get("name")
    price = data.get("price")
    new_add_to_cart = Add_To_Cart(product_id=product_id,user_id=user_id,quantity=quantity,name=name,price=price)
    db.session.add(new_add_to_cart)
    db.session.commit()
@app.route('/delete_cart', methods=['POST'])
def delete_cart():
    data = request.get_json()
    cart_id = data.get("cart_id")
    cart = Add_To_Cart.query.filter(Add_To_Cart.id==cart_id).first()
    db.session.delete(cart)
    db.session.commit()
@app.route('/view_cart', methods=['POST'])
def view_cart():
    data = request.get_json()
    user_id = data.get("user_id")
    user_cart = Add_To_Cart.query.filter(Add_To_Cart.user_id==user_id).all()
    total_price=0
    if user_cart:
        for cart in user_cart:
            available_cart = [{"name":cart.name,"price":cart.price,"quantity":cart.quantity} for cart in user_cart]
            total_price = cart.price+total_price
    return jsonify({"avaliable_cart":available_cart,"total_price":total_price})
if __name__ == '__main__':
    app.run(debug=True)