# app/routes/api.py
# ============================================================================
# INTERNAL API ENDPOINTS (For system integration)
# ============================================================================
@api_bp.route('/internal/sync', methods=['POST'])
@login_required
def internal_sync():
    """Internal data synchronization endpoint."""
    # TODO: Implement internal sync logic
    return jsonify({
        'message': 'Sync completed successfully',
        'timestamp': datetime.utcnow().isoformat()
    })
@api_bp.route('/internal/maintenance', methods=['POST'])
@login_required
def internal_maintenance():
    """Internal maintenance operations."""
    # TODO: Implement maintenance operations
    operation = request.get_json().get('operation') if request.get_json() else None
    return jsonify({
        'message': f'Maintenance operation {operation} completed',
        'timestamp': datetime.utcnow().isoformat()
    })
# ============================================================================
# DIGITAL PRODUCT GENERATION ENDPOINT
# ============================================================================

# Import required for digital product generation
from app.utils.digital_product import generate_digital_product

@api_bp.route('/products/generate', methods=['POST'])
@login_required
def generate_product():
    """Generate a new digital product (API)."""
    try:
        data = request.get_json()
        if not data or not data.get('product_spec'):
            abort(400, description="Missing product_spec in request body.")
        product = generate_digital_product(data['product_spec'], user_id=current_user.get_id())
        return jsonify({'success': True, 'product': product}), 201
    except Exception as exc:
        logging.error(f"Product generation failed: {exc}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate digital product',
            'details': str(exc)
        }), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================
@api_bp.errorhandler(404)
def api_not_found(error):
    """Handle 404 errors for API routes."""
    return jsonify({
        'error': 'API endpoint not found',
        'message': 'The requested API endpoint does not exist'
    }), 404
@api_bp.errorhandler(400)
def api_bad_request(error):
    """Handle 400 errors for API routes."""
    return jsonify({
        'error': 'Bad request',
        'message': 'The request was invalid or malformed'
    }), 400
@api_bp.errorhandler(500)
def api_internal_error(error):
    """Handle 500 errors for API routes."""
    logging.error(f'API Internal Error: {error}')
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500
# API blueprint ready for registration with Flask app
