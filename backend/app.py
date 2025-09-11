from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from ai_categorization import ai_analyzer
from receipt_parser import extract_receipt_data, parse_receipt
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)

# Local database configuration
def get_database_url():
    # For local development only
    return os.getenv('DATABASE_URL', 'sqlite:///expense_tracker.db')

# Configuration - Secure version
secret_key = os.getenv('SECRET_KEY')
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

if not secret_key or not jwt_secret_key:
    raise ValueError("SECRET_KEY and JWT_SECRET_KEY must be set in environment variables")

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expenses = db.relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat()
        }

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'merchant': self.merchant,
            'amount': self.amount,
            'description': self.description,
            'category': self.category,
            'payment_method': self.payment_method,
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }

# Routes


# Users
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters long'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'error': 'Username not found', 'error_type': 'invalid_username'}), 401
        if not user.check_password(password):
            return jsonify({'error': 'Invalid password', 'error_type': 'invalid_password'}), 401

        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Expenses
@app.route('/api/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    try:
        user_id = int(get_jwt_identity())
        expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc(), Expense.created_at.desc()).all()
        return jsonify([expense.to_dict() for expense in expenses]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['merchant', 'description', 'amount', 'category', 'payment_method', 'date']
        for field in required_fields:
            field_value = data.get(field)
            if field not in data or not field_value or str(field_value).strip() == '':
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400
        
        # Validate description and category
        merchant_stripped = data['merchant'].strip()
        desc_stripped = data['description'].strip()
        cat_stripped = data['category'].strip()
        payment_method_stripped = data['payment_method'].strip()

        if not desc_stripped:
            return jsonify({'error': 'Description cannot be empty'}), 400
        if not cat_stripped:
            return jsonify({'error': 'Category cannot be empty'}), 400

        # Validate date
        try:
            expense_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        expense = Expense(
            merchant=merchant_stripped,
            description=desc_stripped,
            amount=amount,
            category=cat_stripped,
            payment_method=payment_method_stripped,
            date=expense_date,
            user_id=user_id
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify({
            'message': 'Expense added successfully',
            'expense': expense.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    try:
        user_id = int(get_jwt_identity())
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        
        if not expense:
            return jsonify({'error': 'Expense not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'merchant' in data:
            expense.merchant = data['merchant'].strip()
            
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    return jsonify({'error': 'Amount must be greater than 0'}), 400
                expense.amount = amount
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid amount format'}), 400
        
        if 'description' in data:
            expense.description = data['description'].strip()
        
        if 'category' in data:
            expense.category = data['category'].strip()

        if 'payment_method' in data:
            expense.payment_method = data['payment_method'].strip()

        if 'date' in data:
            try:
                expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Expense updated successfully',
            'expense': expense.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    try:
        user_id = int(get_jwt_identity())
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        
        if not expense:
            return jsonify({'error': 'Expense not found'}), 404
        
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/categorize', methods=['POST'])
@jwt_required()
def categorize_expense():
    try:
        data = request.get_json()
        if not data or not data.get('description'):
            return jsonify({'error': 'Description is required'}), 400
        
        description = data['description'].strip()
        category = ai_analyzer.categorize_expense(description)
        
        return jsonify({
            'suggested_category': category,
            'description': description
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/upload-receipt', methods=['POST'])
@jwt_required()
def upload_receipt():
    try:
        user_id = int(get_jwt_identity())
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")  # debug

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # testing
        filename = secure_filename(file.filename)

        # save file temporarily
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)

        # OCR
        print("Starting OCR...")  # debug
        ocr_text = extract_receipt_data(temp_path)

        # save OCR output to a .txt file for testing
        output_dir = os.path.join(os.getcwd(), 'ocr_outputs')
        os.makedirs(output_dir, exist_ok=True)
        
        # create a unique filename for the output text file
        base_filename, _ = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{base_filename}_{timestamp}.txt"
        output_path = os.path.join(output_dir, output_filename)

        # write the extracted text to the file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ocr_text)
            
        print(f"✅ OCR text successfully saved to: {output_path}")
        
        # Parse OCR text with GPT-2
        expense_data = parse_receipt(ocr_text)

        # Attach user_id for saving immediately
        expense_data['user_id'] = user_id

        return jsonify({'parsed_expense': expense_data}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Dashboard
@app.route('/api/dashboard/summary', methods=['GET'])
@jwt_required()
def get_dashboard_summary():
    try:
        user_id = int(get_jwt_identity())
        
        # Get current month expenses for pie chart
        current_month_start = datetime.now().replace(day=1).date()
        next_month = current_month_start.replace(month=current_month_start.month + 1) if current_month_start.month < 12 else current_month_start.replace(year=current_month_start.year + 1, month=1)
        
        current_month_expenses = Expense.query.filter(
            Expense.user_id == user_id,
            Expense.date >= current_month_start,
            Expense.date < next_month
        ).all()
        
        # Category breakdown for pie chart
        category_totals = {}
        for expense in current_month_expenses:
            category = expense.category
            if category in category_totals:
                category_totals[category] += expense.amount
            else:
                category_totals[category] = expense.amount
        
        # Last 30 days for bar chart
        thirty_days_ago = (datetime.now() - timedelta(days=30)).date()
        last_30_days_expenses = Expense.query.filter(
            Expense.user_id == user_id,
            Expense.date >= thirty_days_ago
        ).all()
        
        # Daily totals for bar chart
        daily_totals = {}
        for expense in last_30_days_expenses:
            date_str = expense.date.isoformat()
            if date_str in daily_totals:
                daily_totals[date_str] += expense.amount
            else:
                daily_totals[date_str] = expense.amount
        
        # Fill in missing days with 0
        current_date = thirty_days_ago
        while current_date <= datetime.now().date():
            date_str = current_date.isoformat()
            if date_str not in daily_totals:
                daily_totals[date_str] = 0
            current_date += timedelta(days=1)
        
        # Sort daily totals by date
        sorted_daily_totals = dict(sorted(daily_totals.items()))
        
        return jsonify({
            'category_breakdown': category_totals,
            'daily_spending': sorted_daily_totals,
            'total_current_month': sum(category_totals.values()),
            'total_last_30_days': sum(daily_totals.values())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/insights', methods=['GET'])
@jwt_required()
def get_ai_insights():
    try:
        user_id = int(get_jwt_identity())
        
        # Get last 30 days of expenses
        thirty_days_ago = (datetime.now() - timedelta(days=30)).date()
        expenses = Expense.query.filter(
            Expense.user_id == user_id,
            Expense.date >= thirty_days_ago
        ).all()
        
        expenses_data = [expense.to_dict() for expense in expenses]
        insights = ai_analyzer.get_spending_insights(expenses_data)
        
        return jsonify({
            'insights': insights,
            'period': '30 days',
            'total_expenses': len(expenses_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Personal Expense Tracker (PET) API',
        'version': '1.0',
        'description': 'Personal finance management API',
        'documentation': 'https://github.com/chickenbake/Personal-Expense-Tracker',
        'endpoints': {
            'health': {
                'url': '/api/health',
                'method': 'GET',
                'description': 'Check API health status'
            },
            'register': {
                'url': '/api/register',
                'method': 'POST',
                'description': 'Create new user account'
            },
            'login': {
                'url': '/api/login',
                'method': 'POST', 
                'description': 'User authentication'
            },
            'expenses': {
                'url': '/api/expenses',
                'methods': ['GET', 'POST'],
                'description': 'Manage expenses (requires authentication)'
            },
            'dashboard': {
                'url': '/api/dashboard/summary',
                'method': 'GET',
                'description': 'Get spending analytics (requires authentication)'
            }
        },
        'status': 'operational',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    # For local development only
    with app.app_context():
        try:
            db.create_all()
            print("Local: Database tables created")
        except Exception as e:
            print(f"Local: Database error: {e}")
    app.run(debug=True, host='0.0.0.0', port=5001)
