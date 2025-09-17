from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from ..schemas import AccountSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Account
import random
from .. import db

account_bp = Blueprint('account_bp', __name__)
account_schema = AccountSchema()

@account_bp.route('/create', methods=['POST'])
@jwt_required()
def create_account():

    user_id = get_jwt_identity()
    json_data = request.get_json()

    if not json_data:
        return jsonify({"message" : "missing json data"})
    
    account_num = ''.join(random.choices('01234789', k=10))
    json_data['user_id'] = user_id
    json_data['account_num'] = account_num

    data = account_schema.load(json_data)
        
        # Create a new Account object
    new_account = Account(
        user_id=data['user_id'],
        account_num=data['account_num'],
        account_type=data['account_type']
    )
    
    db.session.add(new_account)
    db.session.commit()

    return account_schema.dump(new_account)
    
