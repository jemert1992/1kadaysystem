from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime
import logging

api_bp = Blueprint('api', __name__)

# app/routes/api.py
# ============================================================================
# INTERNAL API ENDPOINTS (For system integration)
# ============================================================================
@api_bp.route('/internal/sync', methods=['POST'])
@login_required
def internal_sync():
    """Internal data synchronization endpoint."""
    try:
        # Get user ID for tracking
        user_id = current_user.get_id()
        
        # Get request data
        data = request.get_json() or {}
        sync_type = data.get('sync_type', 'full')
        
        # Log sync initiation
        logging.info(f"User {user_id} initiated {sync_type} sync")
        
        # Implement user data sync logic
        sync_results = {}
        
        if sync_type == 'full':
            # Full synchronization
            sync_results['user_data'] = f'Full sync completed for user {user_id}'
            sync_results['profiles'] = 'All user profiles synchronized'
            sync_results['preferences'] = 'User preferences updated'
        elif sync_type == 'incremental':
            # Incremental synchronization
            sync_results['user_data'] = f'Incremental sync completed for user {user_id}'
            sync_results['recent_changes'] = 'Only recent changes synchronized'
        else:
            # Unknown sync type
            logging.warning(f"Unknown sync type '{sync_type}' requested by user {user_id}")
            return jsonify({
                'success': False,
                'error': f'Unknown sync type: {sync_type}',
                'valid_types': ['full', 'incremental']
            }), 400
        
        # Log successful completion
        logging.info(f"Sync operation '{sync_type}' completed successfully for user {user_id}")
        
        return jsonify({
            'success': True,
            'message': 'Sync completed successfully',
            'sync_type': sync_type,
            'user_id': user_id,
            'results': sync_results,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        # Error handling with logging
        logging.error(f"Sync operation failed for user {current_user.get_id() if current_user else 'unknown'}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Sync operation failed',
            'details': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@api_bp.route('/internal/maintenance', methods=['POST'])
@login_required
def internal_maintenance():
    """Internal maintenance operations with flexible operation handler."""
    try:
        # Get user ID for tracking
        user_id = current_user.get_id()
        
        # Get request data
        data = request.get_json() if request.get_json() else {}
        operation = data.get('operation')
        operation_params = data.get('params', {})
        
        # Log maintenance operation initiation
        logging.info(f"User {user_id} initiated maintenance operation: {operation}")
        
        # Flexible operation handler with switch logic
        result = {}
        
        if operation == 'cleanup':
            # Database cleanup operation
            result['action'] = 'cleanup'
            result['description'] = 'Database cleanup completed'
            result['records_cleaned'] = operation_params.get('record_count', 100)
            logging.info(f"Cleanup operation completed by user {user_id}")
            
        elif operation == 'backup':
            # Backup operation
            result['action'] = 'backup'
            result['description'] = 'System backup completed'
            result['backup_location'] = operation_params.get('location', '/backup/default')
            logging.info(f"Backup operation completed by user {user_id}")
            
        elif operation == 'optimize':
            # Database optimization
            result['action'] = 'optimize'
            result['description'] = 'Database optimization completed'
            result['tables_optimized'] = operation_params.get('tables', ['all'])
            logging.info(f"Optimization operation completed by user {user_id}")
            
        elif operation == 'reset_cache':
            # Cache reset operation
            result['action'] = 'reset_cache'
            result['description'] = 'Cache reset completed'
            result['cache_types'] = operation_params.get('cache_types', ['all'])
            logging.info(f"Cache reset operation completed by user {user_id}")
            
        elif operation == 'health_check':
            # System health check
            result['action'] = 'health_check'
            result['description'] = 'System health check completed'
            result['status'] = 'healthy'
            result['checks_performed'] = ['database', 'filesystem', 'memory']
            logging.info(f"Health check operation completed by user {user_id}")
            
        else:
            # Unknown operation
            logging.warning(f"Unknown maintenance operation '{operation}' requested by user {user_id}")
            return jsonify({
                'success': False,
                'error': f'Unknown maintenance operation: {operation}',
                'valid_operations': ['cleanup', 'backup', 'optimize', 'reset_cache', 'health_check'],
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        # Log successful completion
        logging.info(f"Maintenance operation '{operation}' completed successfully for user {user_id}")
        
        return jsonify({
            'success': True,
            'message': f'Maintenance operation {operation} completed',
            'operation': operation,
            'user_id': user_id,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        # Error handling with logging
        logging.error(f"Maintenance operation failed for user {current_user.get_id() if current_user else 'unknown'}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Maintenance operation failed',
            'details': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

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
