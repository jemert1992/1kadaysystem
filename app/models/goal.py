"""Goal model for the 1K A Day System."""

from datetime import datetime, date
from decimal import Decimal
from app import db
from sqlalchemy import func

class Goal(db.Model):
    """Goal model for tracking income goals and targets."""
    
    __tablename__ = 'goal'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    target_amount = db.Column(db.Decimal(10, 2), nullable=False)
    target_date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), default='active', nullable=False)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, user_id, target_amount, target_date, title=None, description=None, status='active'):
        self.user_id = user_id
        self.target_amount = Decimal(str(target_amount)) if not isinstance(target_amount, Decimal) else target_amount
        self.target_date = target_date
        self.title = title
        self.description = description
        self.status = status
    
    def __repr__(self):
        return f'<Goal {self.target_amount} by {self.target_date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_amount': float(self.target_amount),
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'status': self.status,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def is_active(self):
        """Check if goal is active."""
        return self.status == 'active'
    
    def is_completed(self):
        """Check if goal is completed."""
        return self.status == 'completed'
    
    def mark_completed(self):
        """Mark goal as completed."""
        self.status = 'completed'
        self.updated_at = datetime.utcnow()
    
    def mark_active(self):
        """Mark goal as active."""
        self.status = 'active'
        self.updated_at = datetime.utcnow()
    
    @staticmethod
    def get_user_active_goals(user_id):
        """Get all active goals for a user."""
        return Goal.query.filter_by(user_id=user_id, status='active').order_by(Goal.target_date).all()
    
    @staticmethod
    def get_user_goals_by_date(user_id, target_date):
        """Get goals for a user by target date."""
        return Goal.query.filter_by(user_id=user_id, target_date=target_date).all()
