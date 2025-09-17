from flask import Blueprint, jsonify, request
from ..schemas import TransactionSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Account
from ..models import Transaction
from . import db
import datetime
from marshmallow import ValidationError

transaction_bp = Blueprint('transaction_bp', __name__)
transaction_schema = TransactionSchema()


@transaction_bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    json_data = request.get_json()

    if not json_data:
        return jsonify({"message" : "json data is missing"})
    
    try:
        data = transaction_schema.load(json_data)

        from_account_id = data.get('from_account_id')
        to_account_id = data.get('to_account_id')
        amount = data.get('amount')

        if not from_account_id or not to_account_id:
            return jsonify({"message" : "missing account id"})
        
        from_account = Account.query.get(from_account_id)
        to_account = Account.query.get(to_account_id)

        if not from_account and not to_account:
            return jsonify({"message" : "invalid account id"})
        
        if from_account.id == to_account.id:
            return jsonify({"message" : "cannot transfer to the same account"})
        
        if str(from_account.user_id) != user_id:
            return jsonify({"message" : "you are not authorized to perform this transaction "})
        
        try:
            from_account.debit_balance(amount)
        except ValueError as e:
            return jsonify({"message" : str(e)})
        
        to_account.credit_balance(amount)
        
        new_transaction = Transaction(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            transaction_type='transfer',
            timestamp=datetime.datetime.utcnow()
        )
        
        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({"message" : "Transaction successful"})
    
    except ValidationError as err:
        return jsonify(err.messages)
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500