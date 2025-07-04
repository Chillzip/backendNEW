import os
import sys

# Add the project root folder (parent of 'src') to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import stripe

from src.models.user import db, User
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.payment import payment_bp
from src.routes.process import process_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Production configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Removed fallback

# Correctly resolve the absolute path to chillzip.db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # Removed fallback

# Fix for Render PostgreSQL URL (optional)
if app.config['SQLALCHEMY_DATABASE_URI'] and app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Enable CORS for your frontend origin (replace with your actual frontend URL)
CORS(app, supports_credentials=True, origins=['https://www.chillzip.com', 'http://localhost:3000', 'http://localhost:5003'])

# Stripe configuration
app.config['STRIPE_PUBLISHABLE_KEY'] = os.environ.get('STRIPE_PUBLISHABLE_KEY')
app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')
app.config['STRIPE_WEBHOOK_SECRET'] = os.environ.get('STRIPE_WEBHOOK_SECRET')
stripe.api_key = app.config['STRIPE_SECRET_KEY']

# Initialize database
db.init_app(app)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(payment_bp, url_prefix='/api/payment')
app.register_blueprint(process_bp, url_prefix='/api')

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return {
        'status': 'healthy',
        'service': 'ChillZip Backend',
        'message': 'Welcome to ChillZip Backend!',
        'version': '1.0.0'
    }

@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'service': 'ChillZip Backend'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)
