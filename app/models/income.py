"""Income model for the 1K A Day System."""

from datetime import datetime, date, timedelta
from decimal import Decimal
from app import db
from sqlalchemy import func

class Income(db.Model):
    """Income model for tracking daily income records."""
    
    __tablename__ = 'income'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    amount = db.Column(db.Decimal(10, 2), nullable=False)
    source = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, user_id, amount, source=None, description=None, date=None):
        self.user_id = user_id
        self.amount = Decimal(str(amount)) if not isinstance(amount, Decimal) else amount
        self.source = source
        self.description = description
        self.date = date if date else date.today()
    
    def __repr__(self):
        return f'<Income {self.amount} on {self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': float(self.amount),
            'source': self.source,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_by_user_and_date(user_id, target_date):
        return Income.query.filter_by(user_id=user_id, date=target_date).all()
    
    @staticmethod
    def get_total_by_user_and_date(user_id, target_date):
        result = db.session.query(func.sum(Income.amount)).filter_by(
            user_id=user_id, date=target_date).scalar()
        return result if result else Decimal('0.00')
