"""Product model for e-commerce product management and catalog."""

from app import db
from datetime import datetime


class Product(db.Model):
    """Product model for managing digital and physical products.
    
    Handles product information, pricing, inventory, and
    metadata for the e-commerce system.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Decimal(10, 2), nullable=False)
    category = db.Column(db.String(100))
    sku = db.Column(db.String(50), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    stock_quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0
    
    def reduce_stock(self, quantity):
        """Reduce stock quantity by specified amount."""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            return True
        return False
