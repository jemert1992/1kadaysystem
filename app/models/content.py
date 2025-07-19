"""Content model for digital product content management.

This module provides the Content model for managing digital product content
including courses, ebooks, templates, and other digital products per the
business blueprint requirements.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app import db
import enum


class ContentType(enum.Enum):
    """Enumeration of supported digital content types."""
    COURSE = "course"
    EBOOK = "ebook"
    TEMPLATE = "template"
    VIDEO = "video"
    AUDIO = "audio"
    SOFTWARE = "software"
    GUIDE = "guide"
    OTHER = "other"


class ContentStatus(enum.Enum):
    """Enumeration of content lifecycle status values."""
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DISCONTINUED = "discontinued"


class Content(db.Model):
    """Model for digital product content management.
    
    Manages digital products including courses, ebooks, templates, and other
    content types with comprehensive metadata, versioning, and analytics support.
    Supports the 1k-a-day system's digital product strategy.
    """
    
    __tablename__ = 'contents'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    
    # Content classification
    content_type = Column(Enum(ContentType), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    tags = Column(Text, nullable=True)  # JSON or comma-separated tags
    
    # Content details
    description = Column(Text, nullable=True)
    content_body = Column(Text, nullable=True)  # Main content or summary
    excerpt = Column(Text, nullable=True)  # Short description for listings
    
    # Media and assets
    featured_image_url = Column(String(500), nullable=True)
    download_url = Column(String(500), nullable=True)  # For downloadable content
    preview_url = Column(String(500), nullable=True)  # For previews/demos
    file_size = Column(Integer, nullable=True)  # File size in bytes
    file_format = Column(String(50), nullable=True)  # PDF, MP4, ZIP, etc.
    
    # Pricing and commerce
    price = Column(Numeric(10, 2), nullable=True, default=0.00)
    original_price = Column(Numeric(10, 2), nullable=True)  # For sales/discounts
    is_free = Column(Boolean, nullable=False, default=False)
    requires_subscription = Column(Boolean, nullable=False, default=False)
    
    # Content management
    status = Column(Enum(ContentStatus), nullable=False, default=ContentStatus.DRAFT, index=True)
    version = Column(String(20), nullable=True, default='1.0')
    is_featured = Column(Boolean, nullable=False, default=False)
    is_premium = Column(Boolean, nullable=False, default=False)
    
    # SEO and marketing
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(String(300), nullable=True)
    keywords = Column(Text, nullable=True)
    
    # Analytics and engagement
    view_count = Column(Integer, nullable=False, default=0)
    download_count = Column(Integer, nullable=False, default=0)
    rating_average = Column(Numeric(3, 2), nullable=True)  # 0.00 to 5.00
    rating_count = Column(Integer, nullable=False, default=0)
    
    # Access control
    is_public = Column(Boolean, nullable=False, default=True)
    access_level = Column(String(50), nullable=True)  # public, member, premium, etc.
    
    # Relationships
    created_by_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    updated_by_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    # Relationships
    created_by = relationship('User', foreign_keys=[created_by_id], backref='created_contents')
    updated_by = relationship('User', foreign_keys=[updated_by_id], backref='updated_contents')
    
    def __repr__(self):
        """String representation of Content instance."""
        return f'<Content {self.id}: {self.title} ({self.content_type.value})>'
    
    def to_dict(self):
        """Convert Content instance to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content_type': self.content_type.value if self.content_type else None,
            'category': self.category,
            'description': self.description,
            'excerpt': self.excerpt,
            'price': float(self.price) if self.price else 0.00,
            'is_free': self.is_free,
            'status': self.status.value if self.status else None,
            'is_featured': self.is_featured,
            'is_premium': self.is_premium,
            'view_count': self.view_count,
            'download_count': self.download_count,
            'rating_average': float(self.rating_average) if self.rating_average else None,
            'rating_count': self.rating_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
    
    @classmethod
    def get_published(cls):
        """Get all published content."""
        return cls.query.filter_by(status=ContentStatus.PUBLISHED).all()
    
    @classmethod
    def get_by_type(cls, content_type):
        """Get content filtered by type."""
        return cls.query.filter_by(content_type=content_type).all()
    
    @classmethod
    def get_featured(cls):
        """Get featured content."""
        return cls.query.filter_by(is_featured=True, status=ContentStatus.PUBLISHED).all()
    
    def increment_view_count(self):
        """Increment the view count for analytics."""
        self.view_count += 1
        db.session.commit()
    
    def increment_download_count(self):
        """Increment the download count for analytics."""
        self.download_count += 1
        db.session.commit()
    
    def publish(self):
        """Publish the content."""
        self.status = ContentStatus.PUBLISHED
        self.published_at = datetime.utcnow()
        db.session.commit()
    
    def archive(self):
        """Archive the content."""
        self.status = ContentStatus.ARCHIVED
        db.session.commit()
