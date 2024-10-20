from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key


@app.context_processor
def utility_processor():
    def get_user_cart(username):
        users = load_users()
        user = next((user for user in users['users'] if user['username'] == username), None)
        if user and 'cart' in user:
            data = load_data()
            cart_items = []
            for key, quantity in user['cart'].items():
                if key:  # Ensure the key is not empty
                    try:
                        category_id, product_id = map(int, key.split('_'))
                        category = next((cat for cat in data['categories'] if cat['id'] == category_id), None)
                        if category:
                            product = next((prod for prod in category['products'] if prod['id'] == product_id), None)
                            if product:
                                cart_items.append({
                                    'name': product['name'],
                                    'image': product['image'],
                                    'quantity': quantity,
                                    'category_name': category['name'],
                                    'product_id': product_id
                                })
                    except ValueError:
                        continue  # Skip invalid keys
            return cart_items
        return []
    return dict(get_user_cart=get_user_cart)

def load_data():
    with open('produits.json') as f:
        return json.load(f)

def load_users():
    with open('static/database.json') as f:
        return json.load(f)

def save_users(users):
    with open('static/database.json', 'w') as f:
        json.dump(users, f, indent=4)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/drogues')
def drogues():
    data = load_data()
    category = next((cat for cat in data['categories'] if cat['name'] == 'Drogues'), None)
    return render_template('produits.html', category=category)

@app.route('/armes')
def armes():
    data = load_data()
    category = next((cat for cat in data['categories'] if cat['name'] == 'Armes'), None)
    return render_template('produits.html', category=category)


@app.route('/papiers')
def papiers():
    data = load_data()
    category = next((cat for cat in data['categories'] if cat['name'] == 'Papiers'), None)
    return render_template('produits.html', category=category)


@app.route('/services')
def services():
    data = load_data()
    category = next((cat for cat in data['categories'] if cat['name'] == 'Services'), None)
    return render_template('produits.html', category=category)


@app.route('/autres')
def autres():
    data = load_data()
    category = next((cat for cat in data['categories'] if cat['name'] == 'Autres'), None)
    return render_template('produits.html', category=category)

@app.route('/<category_name>/<product_id>')
def product_details(category_name, product_id):
    data = load_data()
    category = next((cat for cat in data['categories'] if cat['name'] == category_name), None)
    product = next((prod for prod in category['products'] if prod['id'] == int(product_id)), None)
    return render_template('product_details.html', product=product, category=category)

'''

    CART IMPLEMENTATION
    
    obligation to be logged in to add to cart
    add to cart: add a dict(tuple:number) = (category_id, product_id):quantity to the user's cart
    remoove product from database + cart when bought

'''

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return json.dumps({'success': False, 'message': 'User not logged in'}), 401, {'ContentType': 'application/json'}

    category_id = int(request.form['category_id'])
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])

    users = load_users()
    user = next((user for user in users['users'] if user['username'] == session['username']), None)

    if user:
        cart_item = f"{category_id}_{product_id}"
        if 'cart' not in user:
            user['cart'] = {}
        if cart_item in user['cart']:
            user['cart'][cart_item] += quantity
        else:
            user['cart'][cart_item] = quantity

        # Vérifier la quantité en stock sans la décrémenter
        data = load_data()
        category = next((cat for cat in data['categories'] if cat['id'] == category_id), None)
        if category:
            product = next((prod for prod in category['products'] if prod['id'] == product_id), None)
            if product:
                if 'quantity' not in product or product['quantity'] >= quantity:
                    save_users(users)
                    return json.dumps({'success': True, 'message': 'Item added to cart'}), 200, {'ContentType': 'application/json'}
                else:
                    return json.dumps({'success': False, 'message': 'Not enough stock available'}), 400, {'ContentType': 'application/json'}
    return json.dumps({'success': False, 'message': 'User not found'}), 404, {'ContentType': 'application/json'}


#TODO l'achat ajoute des item livrer ou en livraison avc une date d'achat
#TODO : implement the cart (add to it + see it + remove from it + buy)
#TODO : Add a route to display the product details
#TODO : Edit the display of the products so its smoother
#TODO : implement the user account (sales history; account balance; address; credit card number; email; password; username; cart; products bought; product in shipping)
#TODO implement the community page (chat, sell from user to user => possibility to sell to the website)


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/communaute')
def communaute():
    return render_template('communaute.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')
        credit_card_number = request.form.get('credit_card_number', '')
        address = request.form.get('address', '')

        users = load_users()
        if any(user['username'] == username for user in users['users']):
            error_message = "Username already exists. Please try to log in."
            return render_template('register.html', error_message=error_message)

        new_user = {
            "username": username,
            "password": password,
            "email": email,
            "cart": [],
            "credit_card_number": credit_card_number,
            "account_balance": 0,
            "address": address,
            "sales": []
        }
        users['users'].append(new_user)
        save_users(users)
        session['username'] = username
        return redirect(url_for('home'))

    return render_template('register.html', error_message=error_message)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    users = load_users()
    user = next((user for user in users['users'] if user['username'] == username and user['password'] == password), None)
    if user:
        session['username'] = username
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False, 'error_message': "Invalid username or password."}), 401, {'ContentType': 'application/json'}

@app.route('/logout')
def logout():
    previous_url = request.referrer
    session.pop('username', None)
    return redirect(previous_url)

if __name__ == '__main__':
    app.run()