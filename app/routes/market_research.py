from flask import Blueprint, jsonify
from app.services.market_research_service import MarketResearchService

market_research_bp = Blueprint('market_research', __name__)

@market_research_bp.route('/api/market-research', methods=['GET'])
def get_market_research_report():
    """API endpoint for automated market research report."""
    try:
        service = MarketResearchService()
        report = service.summary_report()
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
