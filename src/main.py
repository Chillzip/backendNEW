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

app = Flask(__name__, static_folder="../frontend/dist/static", static_url_path="/static")

# Configs
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chillzip.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "8caff4c6ee3cbf33dd5f3f468541325bf61d337b4d90e34e4d6668a87164fe42"

db.init_app(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

CORS(app, resources={r"/api/*": {"origins": "*"}})

stripe.api_key = "sk_test_..."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(process_bp)

@app.route("/")
def index():
    return send_from_directory("../frontend/dist", "index.html")

if __name__ == "__main__":
    app.run(debug=True)
