"""Setting model for global application configuration.

This module provides the Setting model for storing key-value pairs
for global application configuration settings.
"""

from sqlalchemy import Column, Integer, String, Text
from app.database import db


class Setting(db.Model):
    """Model for storing global application configuration settings.
    
    This model provides a flexible key-value store for application
    configuration that can be modified at runtime without code changes.
    
    Attributes:
        id (int): Primary key for the setting record
        key (str): Unique configuration key identifier
        value (str): Configuration value stored as text
    """
    
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    
    def __init__(self, key, value=None):
        """Initialize a new Setting instance.
        
        Args:
            key (str): The configuration key
            value (str, optional): The configuration value
        """
        self.key = key
        self.value = value
    
    def __repr__(self):
        """Return string representation of the Setting.
        
        Returns:
            str: String representation showing key and value
        """
        return f'<Setting {self.key}: {self.value}>'
    
    @classmethod
    def get_value(cls, key, default=None):
        """Get a setting value by key.
        
        Args:
            key (str): The configuration key to retrieve
            default: Default value if key not found
            
        Returns:
            The setting value or default if not found
        """
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @classmethod
    def set_value(cls, key, value):
        """Set a setting value by key.
        
        Args:
            key (str): The configuration key
            value: The value to set
            
        Returns:
            Setting: The created or updated Setting instance
        """
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = cls(key=key, value=value)
            db.session.add(setting)
        
        db.session.commit()
        return setting
