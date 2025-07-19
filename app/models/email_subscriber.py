"""Email subscriber model for newsletter and marketing management."""

from app import db
from datetime import datetime


class EmailSubscriber(db.Model):
    """Email subscriber model for managing newsletter subscriptions.
    
    Handles email list management, subscription preferences,
    and marketing automation data.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    subscription_source = db.Column(db.String(100))  # landing_page, popup, manual
    interests = db.Column(db.Text)  # JSON string of interests
    last_email_sent = db.Column(db.DateTime)
    unsubscribed_at = db.Column(db.DateTime)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EmailSubscriber {self.email}>'
    
    def unsubscribe(self):
        """Unsubscribe user from emails."""
        self.is_active = False
        self.unsubscribed_at = datetime.utcnow()
    
    def get_full_name(self):
        """Get subscriber's full name."""
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.first_name or self.email
