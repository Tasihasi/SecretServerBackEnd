from flask import current_app as app, render_template
from flask import Blueprint, request, jsonify
from ..model import GetData, PostData
from .Is_valid_request import is_valid_request
from dicttoxml import dicttoxml


# Create a blueprint instance
main_blueprint = Blueprint('main', __name__)

def dict_to_xml(data):
    """Convert dictionary to XML format."""
    return dicttoxml(data).decode('utf-8')

@main_blueprint.route("/")
def home():
    return "<p>Hello, World!</p>"


# Route to handle POST request for creating a new secret and GET for retrieving it by hash
@main_blueprint.route("/secret", methods=['POST']) 
def save_secret():
    if not is_valid_request(request):
        return jsonify({"Error": "Invalid input"}), 405
    
    
    try:
        # Parse JSON data (form data is for simple forms, but you want JSON here)
        data = request.get_json()  # This will parse the JSON body sent from the React app
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
    