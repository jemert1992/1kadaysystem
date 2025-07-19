"""Analytics model for tracking site and business metrics.

This module contains the Analytics model which provides functionality for
tracking various events, user interactions, and business metrics across
the 1K-a-Day system.
"""

from datetime import datetime
from app import db


class Analytics(db.Model):
    """Analytics model for tracking events, user interactions, and business metrics.
    
    This model captures various analytics data points including:
    - User interactions and events
    - Business metrics and KPIs
    - Performance statistics
    - Custom event tracking
    """
    
    __tablename__ = 'analytics'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Event tracking fields
    event_type = db.Column(db.String(100), nullable=False, index=True)
    event_name = db.Column(db.String(200), nullable=False)
    event_category = db.Column(db.String(100), nullable=True, index=True)
    
    # User and session tracking
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    session_id = db.Column(db.String(100), nullable=True, index=True)
    ip_address = db.Column(db.String(45), nullable=True)  # Supports IPv6
    user_agent = db.Column(db.Text, nullable=True)
    
    # Business metrics
    revenue_amount = db.Column(db.Decimal(10, 2), nullable=True)
    conversion_value = db.Column(db.Decimal(10, 2), nullable=True)
    goal_achieved = db.Column(db.Boolean, default=False)
    
    # Performance metrics
    page_load_time = db.Column(db.Float, nullable=True)
    response_time = db.Column(db.Float, nullable=True)
    error_count = db.Column(db.Integer, default=0)
    
    # Custom data fields
    custom_data = db.Column(db.JSON, nullable=True)  # For flexible event data
    tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags
    
    # Metadata
    url_path = db.Column(db.String(500), nullable=True)
    referrer = db.Column(db.String(500), nullable=True)
    utm_source = db.Column(db.String(100), nullable=True)
    utm_medium = db.Column(db.String(100), nullable=True)
    utm_campaign = db.Column(db.String(200), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    processed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='analytics_events', lazy=True)
    
    def __init__(self, event_type, event_name, **kwargs):
        """Initialize Analytics instance.
        
        Args:
            event_type (str): Type of event (e.g., 'pageview', 'click', 'purchase')
            event_name (str): Name of the specific event
            **kwargs: Additional fields to set
        """
        self.event_type = event_type
        self.event_name = event_name
        
        # Set additional fields from kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self):
        """String representation of Analytics instance."""
        return f'<Analytics {self.event_type}:{self.event_name} at {self.created_at}>'
    
    def to_dict(self):
        """Convert Analytics instance to dictionary.
        
        Returns:
            dict: Dictionary representation of the analytics event
        """
        return {
            'id': self.id,
            'event_type': self.event_type,
            'event_name': self.event_name,
            'event_category': self.event_category,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'revenue_amount': float(self.revenue_amount) if self.revenue_amount else None,
            'conversion_value': float(self.conversion_value) if self.conversion_value else None,
            'goal_achieved': self.goal_achieved,
            'custom_data': self.custom_data,
            'url_path': self.url_path,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def track_event(cls, event_type, event_name, **kwargs):
        """Class method to easily track new events.
        
        Args:
            event_type (str): Type of event
            event_name (str): Name of the event
            **kwargs: Additional event data
            
        Returns:
            Analytics: Created analytics instance
        """
        analytics = cls(event_type=event_type, event_name=event_name, **kwargs)
        db.session.add(analytics)
        db.session.commit()
        return analytics
    
    @classmethod
    def get_events_by_type(cls, event_type, limit=100):
        """Get recent events by type.
        
        Args:
            event_type (str): Type of events to retrieve
            limit (int): Maximum number of events to return
            
        Returns:
            list: List of Analytics instances
        """
        return cls.query.filter_by(event_type=event_type).order_by(
            cls.created_at.desc()
        ).limit(limit).all()
    
    @classmethod
    def get_revenue_stats(cls, start_date=None, end_date=None):
        """Get revenue statistics for a date range.
        
        Args:
            start_date (datetime): Start date for the range
            end_date (datetime): End date for the range
            
        Returns:
            dict: Revenue statistics
        """
        query = cls.query.filter(cls.revenue_amount.isnot(None))
        
        if start_date:
            query = query.filter(cls.created_at >= start_date)
        if end_date:
            query = query.filter(cls.created_at <= end_date)
        
        total_revenue = db.session.query(
            db.func.sum(cls.revenue_amount)
        ).filter(
            cls.revenue_amount.isnot(None)
        ).scalar() or 0
        
        event_count = query.count()
        
        return {
            'total_revenue': float(total_revenue),
            'event_count': event_count,
            'average_revenue': float(total_revenue / event_count) if event_count > 0 else 0
        }
