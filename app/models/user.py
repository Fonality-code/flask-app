"""
User model
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from typing import Any


class User(UserMixin, db.Model):
    """User model for authentication and user management"""

    __tablename__ = 'users'

    # Primary fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Personal information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)

    # Location information
    country = db.Column(db.String(2), nullable=False)  # ISO country code
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)

    # Account settings
    preferred_language = db.Column(db.String(5), nullable=False, default='en')
    account_type = db.Column(db.String(20), nullable=False, default='customer')  # customer, business, both
    account_status = db.Column(db.String(20), nullable=False, default='active')  # active, inactive, banned
    email_verified = db.Column(db.Boolean, nullable=False, default=False)

    # Business information (optional)
    business_name = db.Column(db.String(100), nullable=True)
    business_type = db.Column(db.String(50), nullable=True)
    business_description = db.Column(db.Text, nullable=True)
    website_url = db.Column(db.String(200), nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    last_login = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password: str):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_business_user(self):
        """Check if user has business account type"""
        return self.account_type in ['business', 'both']

    @property
    def is_customer_user(self):
        """Check if user has customer account type"""
        return self.account_type in ['customer', 'both']

    def to_dict(self) -> dict[str, Any]:
        """Convert user to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'country': self.country,
            'city': self.city,
            'preferred_language': self.preferred_language,
            'account_type': self.account_type,
            'account_status': self.account_status,
            'email_verified': self.email_verified,
            'business_name': self.business_name,
            'business_type': self.business_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
