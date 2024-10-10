from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

def load_data():
    with open('produits.json') as f:
        return json.load(f)

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


if __name__ == '__main__':
    app.run()