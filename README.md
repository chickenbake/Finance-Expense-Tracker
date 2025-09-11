# 💰 Personal Expense Tracker (PET)

A full-stack expense tracking application with AI-powered categorization, built with React and Flask for local development.

## ✨ Features

- **User Authentication**: Secure login/register with JWT tokens
- **Expense Management**: Add, edit, delete, and categorize expenses
- **AI-Powered Categorization**: Automatic expense categorization using Hugging Face models
- **Dashboard Analytics**: Visual charts and spending insights
- **Responsive Design**: Works on desktop and mobile
- **Local Development**: Easy setup for local development environment

## 🧾 OCR Receipt Reader

The application includes an OCR-powered receipt reader for fast expense entry:

- **Receipt Upload:** Upload images or PDFs of receipts directly in the app.
- **Text Extraction:** Uses [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for high-accuracy text extraction from receipts.
- **Custom GPT-2 Model:** Extracted text is processed by a custom GPT-2 model to intelligently parse merchant, amount, date, and line items.
- **Auto-Fill:** Parsed receipt data is automatically filled into the expense form for review and quick saving.

**How it works:**
1. Go to the expense entry form and upload your receipt.
2. The app extracts and parses the receipt details using OCR and AI.
3. Review and confirm the auto-filled expense data before saving.

**Tech Used:**  
- PaddleOCR (Python)  
- Custom GPT-2 model for receipt parsing  
- Integrated with Flask backend

---

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database management
- **JWT** - Authentication and authorization
- **SQLite** - Local development database
- **Hugging Face API** - AI-powered expense categorization

### Frontend
- **React** - Frontend framework
- **Chart.js** - Data visualization
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

## 🏃‍♂️ Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/chickenbake/Finance-Expense-Tracker.git
   cd Finance-Expense-Tracker
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Copy environment template and update with your values
   cp .env.production.template .env
   # Edit .env with your local settings
   
   python app.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Or use the convenience script**
   ```bash
   # On Windows
   start-local-dev.bat
   ```

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001

## 📁 Project Structure

```
Personal-Expense-Tracker-PET/
├── backend/                    # Flask API
│   ├── app.py                 # Main application file
│   ├── ai_service.py          # AI categorization service
│   ├── requirements.txt       # Python dependencies
│   └── .env                  # Environment variables (local)
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── contexts/        # React contexts
│   │   └── services/        # API services
│   ├── public/              # Static assets
│   ├── package.json         # Node.js dependencies
│   ├── Dockerfile          # Frontend container config
│   └── nginx.conf          # Nginx configuration
├── cloudbuild.yaml         # Cloud Build configuration
├── deploy-backend.bat      # Backend deployment script
├── deploy-frontend.bat     # Frontend deployment script
├── start-local-dev.bat    # Local development setup
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

#### Local Development (.env)
```env
SECRET_KEY=your_local_secret_key
JWT_SECRET_KEY=your_local_jwt_secret
HUGGING_FACE_TOKEN=your_hf_token
DATABASE_URL=sqlite:///expense_tracker.db
```

#### Production Example
```env
SECRET_KEY=your_production_secret_key
JWT_SECRET_KEY=your_production_jwt_secret
HUGGING_FACE_TOKEN=your_hf_token
DB_USER=postgres
DB_PASS=your_db_password
DB_NAME=expense_tracker
```

## 🤖 AI Features

The application uses Hugging Face's BART model for intelligent expense categorization:
- Automatically categorizes expenses into predefined categories
- Fallback to keyword-based categorization when AI is unavailable
- Provides spending insights and recommendations

## 🛡️ Security

- JWT-based authentication
- Password hashing with Werkzeug
- CORS configuration for cross-origin requests
- Environment-based secret management
- Non-root user in Docker containers

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/register` - User registration
- `POST /api/login` - User login

### Expense Endpoints
- `GET /api/expenses` - Get user expenses
- `POST /api/expenses` - Add new expense
- `PUT /api/expenses/{id}` - Update expense
- `DELETE /api/expenses/{id}` - Delete expense
- `POST /api/expenses/categorize` - AI categorization

### Dashboard Endpoints
- `GET /api/dashboard/summary` - Dashboard statistics
- `GET /api/insights` - AI spending insights

## 🚨 Troubleshooting

### Common Issues

1. **AI categorization not working**
   - Ensure `HUGGING_FACE_TOKEN` is set in Cloud Run
   - Check Cloud Run logs for API errors

2. **Database connection errors**
   - Verify Cloud SQL instance is running
   - Check connection string and credentials
   - Ensure Cloud SQL proxy is configured

3. **Build failures**
   - Check Dockerfile paths are correct
   - Verify all required files are present
   - Review Cloud Build logs

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review Cloud Build and Cloud Run logs
