from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from ..schemas import AccountSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
import random
from . import db

account_bp = Blueprint('account_bp', __name__)
account_schema = AccountSchema()

@account_bp.route('/account')
@jwt_required()
def create_account():

    user_id = get_jwt_identity()
    json_data = request.get_json()

    if not json_data:
        return jsonify({"message" : "missing json data"})
    
    account_num = ''.join(random.choices('01234789', k=10))
    json_data[user_id] = user_id
    json_data[account_num] = account_num

    new_account = account_schema.load(json_data)
    
    db.session.add(new_account)
    db.session.commit()

    return account_schema.dump(new_account)
    
