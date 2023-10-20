# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'  # Change to your preferred database URI
app.config['SECRET_KEY'] = 'your-secret-key'  # Change to a secure secret key
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from app import routes  # Assuming routes are defined in routes.py

if __name__ == '__main__':
    app.run(debug=True)
