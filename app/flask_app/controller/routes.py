from flask import Blueprint, request, jsonify
from ..model import GetData, PostData
from .Is_valid_request import is_valid_request

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route("/")
def home():
    return "<p>Hello, World!</p>"


# Route to handle POST request for creating a new secret and GET for retrieving it by hash
@main_blueprint.route("/secret", methods=['POST']) 
def save_secret():
    if not is_valid_request(request):
        return jsonify({"Error": "Invalid input"}), 405
    
    try:
        data = request.get_json()
        post_data = PostData(data['secretText'], int(data['retrievalCount']), int(data['expiryDate']))

        if post_data.post_to_db():
            return jsonify({"Hash": post_data.hash}), 200
        else:
            return jsonify({"Error": "Failed to save secret."}), 500

    except (KeyError, ValueError) as e:
        return jsonify({"Error": "Invalid input"}), 405


@main_blueprint.route("/secret/<hash>", methods=['GET']) 
def get_secret(hash):
    try:
        get_data = GetData(hash)

        return get_data.get_secret()

    except Exception as e:
        return jsonify({"Error": "Error retrieving secret."}), 500 