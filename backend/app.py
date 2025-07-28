from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///expense_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-this')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
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
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'category': self.category,
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }

# Routes
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
        
        access_token = create_access_token(identity=user.id)
        
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
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    try:
        user_id = get_jwt_identity()
        expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()
        return jsonify([expense.to_dict() for expense in expenses]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        print(f"Received data: {data}")  # Debug log
        print(f"User ID: {user_id}")     # Debug log
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['amount', 'description', 'category', 'date']
        for field in required_fields:
            if field not in data:
                print(f"Missing field: {field}")  # Debug log
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be greater than 0'}), 400
        except (ValueError, TypeError) as e:
            print(f"Amount validation error: {e}")  # Debug log
            return jsonify({'error': 'Invalid amount format'}), 400
        
        # Validate date
        try:
            expense_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError as e:
            print(f"Date validation error: {e}")  # Debug log
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        expense = Expense(
            amount=amount,
            description=data['description'].strip(),
            category=data['category'].strip(),
            date=expense_date,
            user_id=user_id
        )
        
        db.session.add(expense)
        db.session.commit()
        
        print(f"Expense created successfully: {expense.to_dict()}")  # Debug log
        
        return jsonify({
            'message': 'Expense added successfully',
            'expense': expense.to_dict()
        }), 201
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug log
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    try:
        user_id = get_jwt_identity()
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        
        if not expense:
            return jsonify({'error': 'Expense not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
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
        user_id = get_jwt_identity()
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        
        if not expense:
            return jsonify({'error': 'Expense not found'}), 404
        
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/summary', methods=['GET'])
@jwt_required()
def get_dashboard_summary():
    try:
        user_id = get_jwt_identity()
        
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

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'Backend is working!', 'timestamp': datetime.utcnow().isoformat()}), 200

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
