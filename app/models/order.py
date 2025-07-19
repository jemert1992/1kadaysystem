"""Order model for e-commerce order management and tracking."""

from app import db
from datetime import datetime


class Order(db.Model):
    """Order model for managing customer orders and transactions.
    
    Handles order lifecycle, payment tracking, fulfillment status,
    and customer order history.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Decimal(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')
    payment_status = db.Column(db.String(20), default='unpaid')
    shipping_address = db.Column(db.Text)
    billing_address = db.Column(db.Text)
    stripe_payment_intent_id = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='orders')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    def is_paid(self):
        """Check if order is paid."""
        return self.payment_status == 'paid'
    
    def can_be_cancelled(self):
        """Check if order can be cancelled."""
        return self.status in ['pending', 'processing']
    
    def update_status(self, new_status):
        """Update order status with timestamp."""
        self.status = new_status
        self.updated_at = datetime.utcnow()
