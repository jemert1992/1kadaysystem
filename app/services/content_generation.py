"""Digital Product Generator Service

This service orchestrates market research, AI content creation, and saving to the Content/Product model.
It provides a unified interface for generating complete digital products with market-informed content.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging

from app.models import Content, Product
from app.services.market_research_service import MarketResearchService
from app.services.ai_service import AIService
from app.core.database import get_db

logger = logging.getLogger(__name__)


@dataclass
class ProductGenerationRequest:
    """Request model for digital product generation"""
    topic: str
    target_audience: str
    content_type: str  # 'course', 'ebook', 'video_series', 'workshop', etc.
    market_research_depth: str = 'standard'  # 'basic', 'standard', 'comprehensive'
    ai_creativity_level: float = 0.7  # 0.0 to 1.0
    include_market_validation: bool = True
    

@dataclass
class ProductGenerationResult:
    """Result model for digital product generation"""
    product_id: Optional[int]
    content_id: Optional[int]
    market_research_data: Dict[str, Any]
    generated_content: Dict[str, str]
    validation_score: Optional[float]
    success: bool
    error_message: Optional[str] = None


class DigitalProductGenerator:
    """Service class that orchestrates market research, AI content creation, and product saving"""
    
    def __init__(self):
        self.market_research_service = MarketResearchService()
        self.ai_service = AIService()
        
    async def generate_digital_product(
        self, 
        request: ProductGenerationRequest
    ) -> ProductGenerationResult:
        """Main orchestration method for generating a complete digital product
        
        Args:
            request: ProductGenerationRequest containing all parameters
            
        Returns:
            ProductGenerationResult with generated product data and metadata
        """
        try:
            logger.info(f"Starting digital product generation for topic: {request.topic}")
            
            # Step 1: Conduct market research
            market_data = await self._conduct_market_research(request)
            
            # Step 2: Generate AI content based on market insights
            content_data = await self._generate_ai_content(request, market_data)
            
            # Step 3: Validate market fit (if requested)
            validation_score = None
            if request.include_market_validation:
                validation_score = await self._validate_market_fit(
                    content_data, market_data
                )
            
            # Step 4: Save to database models
            product_id, content_id = await self._save_to_database(
                request, content_data, market_data, validation_score
            )
            
            logger.info(f"Successfully generated digital product. Product ID: {product_id}")
            
            return ProductGenerationResult(
                product_id=product_id,
                content_id=content_id,
                market_research_data=market_data,
                generated_content=content_data,
                validation_score=validation_score,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error in digital product generation: {str(e)}")
            return ProductGenerationResult(
                product_id=None,
                content_id=None,
                market_research_data={},
                generated_content={},
                validation_score=None,
                success=False,
                error_message=str(e)
            )
    
    async def _conduct_market_research(
        self, 
        request: ProductGenerationRequest
    ) -> Dict[str, Any]:
        """Conduct market research using the MarketResearchService
        
        Args:
            request: ProductGenerationRequest containing research parameters
            
        Returns:
            Dictionary containing market research insights
        """
        logger.info("Conducting market research...")
        
        # Use market research service to gather insights
        market_data = await self.market_research_service.analyze_market(
            topic=request.topic,
            target_audience=request.target_audience,
            depth=request.market_research_depth
        )
        
        return market_data
    
    async def _generate_ai_content(
        self, 
        request: ProductGenerationRequest,
        market_data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate AI content based on market research insights
        
        Args:
            request: ProductGenerationRequest containing content parameters
            market_data: Market research data to inform content generation
            
        Returns:
            Dictionary containing generated content sections
        """
        logger.info("Generating AI content...")
        
        # Extract key insights from market research
        market_insights = self._extract_market_insights(market_data)
        
        # Generate content using AI service
        content_data = await self.ai_service.generate_product_content(
            topic=request.topic,
            content_type=request.content_type,
            target_audience=request.target_audience,
            market_insights=market_insights,
            creativity_level=request.ai_creativity_level
        )
        
        return content_data
    
    async def _validate_market_fit(
        self, 
        content_data: Dict[str, str],
        market_data: Dict[str, Any]
    ) -> float:
        """Validate market fit of generated content
        
        Args:
            content_data: Generated content to validate
            market_data: Market research data for comparison
            
        Returns:
            Float score between 0.0 and 1.0 indicating market fit
        """
        logger.info("Validating market fit...")
        
        # Use AI service to analyze content-market alignment
        validation_score = await self.ai_service.validate_market_fit(
            content=content_data,
            market_insights=market_data
        )
        
        return validation_score
    
    async def _save_to_database(
        self,
        request: ProductGenerationRequest,
        content_data: Dict[str, str],
        market_data: Dict[str, Any],
        validation_score: Optional[float]
    ) -> tuple[int, int]:
        """Save generated product and content to database
        
        Args:
            request: Original generation request
            content_data: Generated content data
            market_data: Market research data
            validation_score: Validation score if available
            
        Returns:
            Tuple of (product_id, content_id)
        """
        logger.info("Saving to database...")
        
        db = next(get_db())
        
        try:
            # Create Product record
            product = Product(
                name=content_data.get('title', request.topic),
                description=content_data.get('description', ''),
                product_type=request.content_type,
                target_audience=request.target_audience,
                market_validation_score=validation_score,
                research_data=market_data,
                created_at=datetime.utcnow()
            )
            
            db.add(product)
            db.flush()  # Get the product ID
            
            # Create Content record
            content = Content(
                product_id=product.id,
                title=content_data.get('title', ''),
                body=content_data.get('body', ''),
                content_type=request.content_type,
                metadata={
                    'generation_request': request.__dict__,
                    'market_research': market_data,
                    'ai_parameters': {
                        'creativity_level': request.ai_creativity_level
                    }
                },
                created_at=datetime.utcnow()
            )
            
            db.add(content)
            db.commit()
            
            return product.id, content.id
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def _extract_market_insights(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key insights from market research data
        
        Args:
            market_data: Raw market research data
            
        Returns:
            Dictionary of key insights for content generation
        """
        # Extract relevant insights for AI content generation
        insights = {
            'trends': market_data.get('trends', []),
            'pain_points': market_data.get('pain_points', []),
            'opportunities': market_data.get('opportunities', []),
            'competitor_analysis': market_data.get('competitors', {}),
            'audience_preferences': market_data.get('audience_data', {})
        }
        
        return insights
    
    async def generate_content_outline(
        self, 
        topic: str, 
        content_type: str,
        target_audience: str
    ) -> Dict[str, Any]:
        """Generate a content outline without full product generation
        
        Args:
            topic: Content topic
            content_type: Type of content to generate
            target_audience: Target audience description
            
        Returns:
            Dictionary containing content outline and structure
        """
        logger.info(f"Generating content outline for: {topic}")
        
        # Lightweight market research for outline
        market_data = await self.market_research_service.quick_analysis(
            topic=topic,
            target_audience=target_audience
        )
        
        # Generate outline using AI service
        outline = await self.ai_service.generate_content_outline(
            topic=topic,
            content_type=content_type,
            target_audience=target_audience,
            market_insights=self._extract_market_insights(market_data)
        )
        
        return {
            'outline': outline,
            'market_insights': market_data,
            'estimated_generation_time': self._estimate_generation_time(content_type)
        }
    
    def _estimate_generation_time(self, content_type: str) -> int:
        """Estimate generation time in minutes based on content type
        
        Args:
            content_type: Type of content being generated
            
        Returns:
            Estimated time in minutes
        """
        time_estimates = {
            'ebook': 45,
            'course': 90,
            'video_series': 120,
            'workshop': 60,
            'blog_series': 30,
            'infographic': 15,
            'webinar': 75
        }
        
        return time_estimates.get(content_type, 60)  # Default to 60 minutes
