import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-blue-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/dashboard" className="text-white text-xl font-bold">
              💰 Personal Expense Tracker (PET)
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link
              to="/dashboard"
              className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition duration-200"
            >
              Dashboard
            </Link>
            <Link
              to="/expenses"
              className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition duration-200"
            >
              Expenses
            </Link>
            <div className="flex items-center space-x-4">
              <span className="text-white text-sm">Welcome, {user?.username}!</span>
              <button
                onClick={handleLogout}
                className="bg-blue-700 hover:bg-blue-800 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
