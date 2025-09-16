from marshmallow import Schema, fields, post_load
from .models import User


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    phone_number = fields.Str()
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        # This method runs after validation.
        # 'data' is the dictionary of validated data.
        
        # Pop the password because the User model doesn't have a 'password' field.
        password = data.pop('password')
        
        # Create a User object with the rest of the data.
        user = User(**data)
        
        # Set the password hash on the new object.
        user.set_password(password)
        
        # Return the fully prepared User object.
        return user


class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    account_num = fields.Str(required=True)
    user_id = fields.Int(required=True)
    account_type = fields.Str(required=True)
    balance = fields.Decimal(as_string=True, places=2, dump_only=True)
    status = fields.Str()


class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Decimal(as_string=True, places=2, required=True)
    transaction_type = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)
    from_account_id = fields.Int(allow_none=True) # Allow null for deposits
    to_account_id = fields.Int(allow_none=True)   # Allow null for withdrawals


class LoanSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    loan_type = fields.Str(required=True)
    amount = fields.Decimal(as_string=True, places=2, required=True)
    interest_rate = fields.Decimal(as_string=True, places=2, required=True)
    term_months = fields.Int(required=True)
    status = fields.Str()
    application_date = fields.Date(dump_only=True)
