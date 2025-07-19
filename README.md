# 1K A Day System

## 📋 Project Overview

The 1K A Day System is a comprehensive Flask-based web application designed to help users achieve consistent daily income goals through structured tracking, AI-powered insights, and integrated payment processing. This system combines modern web technologies with intelligent automation to provide a complete solution for income tracking and goal achievement.

## ✨ Features

### Core Functionality
- **Daily Income Tracking**: Log and monitor daily earnings with detailed analytics
- **Goal Setting & Management**: Set, track, and achieve income milestones
- **AI-Powered Insights**: Leverage OpenAI integration for intelligent recommendations
- **Payment Processing**: Secure transactions through Stripe integration
- **User Authentication**: Secure login and registration system
- **Dashboard Analytics**: Comprehensive reporting and visualization
- **Progress Tracking**: Visual progress indicators and achievement metrics

### Advanced Features
- **Cloud Deployment**: Optimized for Replit cloud hosting
- **Responsive Design**: Mobile-first responsive interface
- **Data Export**: Export tracking data in multiple formats
- **Notification System**: Automated reminders and milestone alerts
- **Multi-currency Support**: Track income in various currencies

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External      │
│   (HTML/CSS/JS) │◄──►│   (Flask)       │◄──►│   Services      │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • API Routes    │    │ • OpenAI API    │
│ • Forms         │    │ • Business      │    │ • Stripe API    │
│ • Analytics     │    │   Logic         │    │ • Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Directory Structure

```
1kadaysystem/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── income.py            # Income tracking model
│   │   └── goal.py              # Goal management model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── dashboard.py         # Dashboard routes
│   │   ├── income.py            # Income tracking routes
│   │   └── api.py               # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py        # OpenAI integration
│   │   ├── payment_service.py   # Stripe integration
│   │   └── analytics_service.py # Analytics engine
│   ├── templates/
│   │   ├── base.html            # Base template
│   │   ├── dashboard.html       # Main dashboard
│   │   ├── auth/                # Authentication templates
│   │   └── components/          # Reusable components
│   ├── static/
│   │   ├── css/                 # Stylesheets
│   │   ├── js/                  # JavaScript files
│   │   └── images/              # Static images
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py        # Custom decorators
│       └── helpers.py           # Utility functions
├── migrations/                  # Database migrations
├── tests/
│   ├── test_models.py
│   ├── test_routes.py
│   └── test_services.py
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL or SQLite
- OpenAI API key
- Stripe account and API keys

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jemert1992/1kadaysystem.git
   cd 1kadaysystem
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

### Replit Cloud Deployment

1. **Import to Replit**
   - Fork this repository to your Replit account
   - Replit will automatically detect the Python environment

2. **Configure Secrets**
   - Add environment variables in Replit Secrets
   - Include all variables from `.env.example`

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   python run.py
   ```

## 🔧 Environment Variables

```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///1kadaysystem.db
# For PostgreSQL: postgresql://username:password@localhost/dbname

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Application Settings
PAGINATION_PER_PAGE=20
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## 🛠️ Main Technologies

### Backend Framework
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Flask-Migrate** - Database migration handling
- **Flask-Login** - User session management
- **Flask-WTF** - Form handling and CSRF protection

### AI & Machine Learning
- **OpenAI API** - GPT integration for insights and recommendations
- **NumPy** - Numerical computing for analytics
- **Pandas** - Data manipulation and analysis

### Payment Processing
- **Stripe** - Secure payment processing
- **Stripe Webhooks** - Real-time payment event handling

### Frontend Technologies
- **HTML5** - Modern markup language
- **CSS3** - Styling with Flexbox and Grid
- **JavaScript (ES6+)** - Interactive functionality
- **Chart.js** - Data visualization
- **Bootstrap** - Responsive CSS framework

### Cloud & Deployment
- **Replit** - Cloud development and hosting platform
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **Gunicorn** - WSGI HTTP Server

### Development Tools
- **pytest** - Testing framework
- **Flask-Testing** - Flask-specific testing utilities
- **python-dotenv** - Environment variable management
- **Werkzeug** - WSGI utility library

## 📊 Database Schema

```python
# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
# Income Model
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Decimal(10, 2), nullable=False)
    source = db.Column(db.String(100))
    date = db.Column(db.Date, nullable=False)
    
# Goal Model
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    target_amount = db.Column(db.Decimal(10, 2), nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
```

## 🔒 Security Features

- **CSRF Protection** - Cross-site request forgery prevention
- **Password Hashing** - Secure password storage with bcrypt
- **Session Management** - Secure user session handling
- **Input Validation** - Server-side form validation
- **SQL Injection Prevention** - Parameterized queries with SQLAlchemy
- **Environment Variables** - Sensitive data protection

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_models.py
```

## 📈 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Income Tracking
- `GET /api/income` - Get income records
- `POST /api/income` - Add income record
- `PUT /api/income/<id>` - Update income record
- `DELETE /api/income/<id>` - Delete income record

### Analytics
- `GET /api/analytics/daily` - Daily income analytics
- `GET /api/analytics/monthly` - Monthly income analytics
- `GET /api/analytics/goals` - Goal progress analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, email support@1kadaysystem.com or join our [Discord community](https://discord.gg/1kadaysystem).

---

**Built with ❤️ for consistent income growth**
