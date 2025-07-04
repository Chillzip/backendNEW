from flask import Blueprint

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/pay', methods=['POST'])
def pay():
    return {"message": "Payment route"}