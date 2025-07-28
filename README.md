# Personal Expense Tracker

A full-stack web application for tracking personal expenses with data visualization features.

## Features

### Core Features
- **User Authentication**: Register, login, and logout functionality
- **Expense Management**: Add, edit, delete, and view expenses
- **Data Visualization**: 
  - Pie chart showing spending breakdown by category (current month)
  - Bar chart showing daily spending for the last 30 days
- **Responsive Design**: Works on desktop and mobile devices

### Technical Stack
- **Frontend**: React.js with Tailwind CSS
- **Backend**: Python Flask with SQLAlchemy
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Charts**: Chart.js with react-chartjs-2
- **Authentication**: JWT tokens

## Project Structure

```
Finance Expense Tracker/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   ├── contexts/      # React context providers
│   │   ├── pages/         # Main page components
│   │   ├── services/      # API service functions
│   │   └── App.js         # Main React component
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS configuration
└── README.md              # This file
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables (optional - defaults will work for development):
   ```bash
   # Edit .env file with your preferred values
   SECRET_KEY=your-super-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key
   DATABASE_URL=sqlite:///expense_tracker.db
   ```

6. Run the Flask application:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/register` - Create a new user account
- `POST /api/login` - Login with username and password

### Expenses
- `GET /api/expenses` - Get all expenses for the logged-in user
- `POST /api/expenses` - Add a new expense
- `PUT /api/expenses/<id>` - Update an existing expense
- `DELETE /api/expenses/<id>` - Delete an expense

### Dashboard
- `GET /api/dashboard/summary` - Get dashboard data for charts

## Usage

1. **Register**: Create a new account with a username and password
2. **Login**: Sign in with your credentials
3. **Add Expenses**: Use the "Add Expense" button to record new expenses
4. **View Dashboard**: See your spending patterns with interactive charts
5. **Manage Expenses**: Edit or delete existing expenses from the Expenses page

## Expense Categories

The application supports the following expense categories:
- Food
- Transport
- Entertainment
- Shopping
- Bills
- Healthcare
- Education
- Travel
- Other

## Development Roadmap

### Phase 1: ✅ Core Features Completed
- User authentication
- Basic expense CRUD operations
- Data visualization
- Responsive UI

### Phase 2: Planned Enhancements
- Monthly budgets and budget tracking
- Search and filter functionality
- Export data to CSV
- Recurring expenses

### Phase 3: Advanced Features
- File upload for receipts
- Multiple currencies support
- Expense categories customization
- Email notifications

## Deployment

### Backend Deployment
The Flask backend can be deployed to platforms like:
- Heroku
- Render
- DigitalOcean App Platform
- AWS Elastic Beanstalk

### Frontend Deployment
The React frontend can be deployed to:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

### Database
For production, consider upgrading from SQLite to:
- PostgreSQL (recommended)
- MySQL
- MongoDB

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or issues, please create an issue in the repository or contact the development team.
