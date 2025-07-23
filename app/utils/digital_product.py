"""Digital Product Utilities

Utility functions for generating and managing digital products.
"""

from typing import Dict, List, Optional, Any
import json
import uuid
from datetime import datetime


def generate_digital_product(
    name: str,
    product_type: str = "course",
    price: float = 0.0,
    description: Optional[str] = None,
    features: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate a digital product with basic structure and metadata.
    
    Args:
        name (str): Name of the digital product
        product_type (str): Type of product (course, ebook, software, etc.)
        price (float): Price of the product
        description (str, optional): Product description
        features (List[str], optional): List of product features
        metadata (Dict[str, Any], optional): Additional metadata
        
    Returns:
        Dict[str, Any]: Generated digital product structure
    """
    if features is None:
        features = []
        
    if metadata is None:
        metadata = {}
    
    product = {
        "id": str(uuid.uuid4()),
        "name": name,
        "type": product_type,
        "price": price,
        "description": description or f"A {product_type} product: {name}",
        "features": features,
        "created_at": datetime.utcnow().isoformat(),
        "status": "draft",
        "metadata": metadata
    }
    
    return product


def validate_product_data(product: Dict[str, Any]) -> bool:
    """
    Validate digital product data structure.
    
    Args:
        product (Dict[str, Any]): Product data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ["id", "name", "type", "price"]
    
    for field in required_fields:
        if field not in product:
            return False
            
    return True


def format_product_for_export(product: Dict[str, Any]) -> str:
    """
    Format product data for export (JSON).
    
    Args:
        product (Dict[str, Any]): Product data
        
    Returns:
        str: JSON formatted product data
    """
    return json.dumps(product, indent=2, default=str)
