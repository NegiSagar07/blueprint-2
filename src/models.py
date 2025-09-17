from . import db
import datetime
from sqlalchemy.sql import func # pyright: ignore[reportMissingImports]
from werkzeug.security import check_password_hash, generate_password_hash

import enum


class LoanStatus(enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    PAID = 'PAID'


class AccountStatus(enum.Enum):
    active = 'active'
    inactive = 'inactive'
    closed = 'closed'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    accounts = db.relationship('Account', back_populates='owner', cascade='all, delete-orphan')
    loans = db.relationship('Loan', back_populates='owner', cascade='all, delete-orphan')


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_num = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_type = db.Column(db.String(40), nullable=True)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=1000.00)
    status = db.Column(db.Enum(AccountStatus), nullable=True, default=AccountStatus.active)

    owner = db.relationship('User', back_populates='accounts')

    def credit_balance(self, amount):
        self.balance += amount

    def debit_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError('Bhai mehnat kar, tere pas itne pese nahi h jitne tu chahta h !')


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.String(40), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # For transfers, both will be set.
    # For deposit, from_account_id will be NULL.
    # For withdrawal, to_account_id will be NULL.
    from_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)
    to_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)

    # Relationships
    from_account = db.relationship('Account', foreign_keys=[from_account_id])
    to_account = db.relationship('Account', foreign_keys=[to_account_id])


class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    loan_type = db.Column(db.String(40))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(4, 2), nullable=False)
    term_months = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Enum(LoanStatus), nullable=True, default=LoanStatus.PENDING)
    application_date = db.Column(db.Date, nullable=True, default=datetime.date.today)

    owner = db.relationship('User', back_populates='loans')