from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key

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

#TODO : Add a route to display the product details
#TODO : implement the cart (add to it + see it + remove from it + buy)
#TODO : implement the user account (register + login + logout + see his sales history)




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