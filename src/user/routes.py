from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from ..schemas import UserSchema
from ..models import User
from .. import db


user_bp = Blueprint('user_bp', __name__)
user_schema = UserSchema()


@user_bp.route('/register', methods=['POST'])
def register():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message' : 'json_data missing'})
    
    try:
        # Now, .load() returns a complete User object, not a dictionary!
        new_user = user_schema.load(json_data)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    try:
        # The user object is already created, we just need to save it.
        db.session.add(new_user)
        db.session.commit()
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'This email address is already in use.'}), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An unexpected error occurred.'}), 500

    return user_schema.dump(new_user), 201