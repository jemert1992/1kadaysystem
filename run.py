# run.py - Application entry point
from app import create_app

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # This block only runs when the script is executed directly (e.g., python run.py)
    # For production deployments with gunicorn, this block is ignored
    app.run(host='0.0.0.0', port=5000, debug=True)
