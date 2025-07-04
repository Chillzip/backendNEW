from flask import Blueprint, request

process_bp = Blueprint('process', __name__)

@process_bp.route('/process', methods=['POST'])
def process_file():
    data = request.get_json()
    return {"message": "File processed", "data": data}