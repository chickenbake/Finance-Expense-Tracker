import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { expenseService } from '../services/api';

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingExpense, setEditingExpense] = useState(null);

  // Helper function to get today's date in PST (Los Angeles timezone)
  const getTodayPST = () => {
    const today = new Date();
    // Convert to PST (UTC-8) or PDT (UTC-7) depending on daylight saving
    const pstDate = new Date(today.toLocaleString("en-US", {timeZone: "America/Los_Angeles"}));
    
    const year = pstDate.getFullYear();
    const month = String(pstDate.getMonth() + 1).padStart(2, '0');
    const day = String(pstDate.getDate()).padStart(2, '0');
    
    return `${year}-${month}-${day}`;
  };

  const [formData, setFormData] = useState({
    amount: '',
    description: '',
    category: '',
    date: getTodayPST(), // Use PST date
  });
  const [suggestedCategory, setSuggestedCategory] = useState('');
  const [loadingCategory, setLoadingCategory] = useState(false);

  const categories = [
    'Food and Dining',
    'Transportation',
    'Entertainment',
    'Shopping',
    'Bills and Utilities',
    'Healthcare',
    'Education',
    'Travel',
    'Other',
  ];

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = async () => {
    try {
      setLoading(true);
      const data = await expenseService.getExpenses();
      setExpenses(data);
    } catch (error) {
      setError('Failed to load expenses');
      console.error('Expenses error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Add debugging for timezone
    console.log('Current PST date:', getTodayPST());
    console.log('Form date being sent:', formData.date);

    try {
      if (editingExpense) {
        await expenseService.updateExpense(editingExpense.id, formData);
      } else {
        await expenseService.addExpense(formData);
      }
      
      setFormData({
        amount: '',
        description: '',
        category: '',
        date: getTodayPST(), // Reset to PST date
      });
      setShowForm(false);
      setEditingExpense(null);
      fetchExpenses();
    } catch (error) {
      console.error('Error saving expense:', error);
      console.error('Error response:', error.response);
      console.error('Form data sent:', formData);
      setError(error.response?.data?.error || 'Failed to save expense');
    }
  };

  const handleEdit = (expense) => {
    setEditingExpense(expense);
    setFormData({
      amount: expense.amount.toString(),
      description: expense.description,
      category: expense.category,
      date: expense.date,
    });
    setShowForm(true);
  };

  const handleDelete = async (expenseId) => {
    if (window.confirm('Are you sure you want to delete this expense?')) {
      try {
        await expenseService.deleteExpense(expenseId);
        fetchExpenses();
      } catch (error) {
        setError('Failed to delete expense');
      }
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingExpense(null);
    setFormData({
      amount: '',
      description: '',
      category: '',
      date: getTodayPST(), // Reset to PST date
    });
  };

  // Helper function to format dates in PST for display
  const formatDatePST = (dateString) => {
    const date = new Date(dateString + 'T00:00:00'); // Treat as local date
    return date.toLocaleDateString('en-US', {
      timeZone: 'America/Los_Angeles',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // Add this function for AI categorization
  const handleDescriptionChange = async (description) => {
    // Update description first
    setFormData(prev => ({ ...prev, description }));
    
    // Auto-suggest category when description has enough characters
    if (description.length >= 3) {
      setLoadingCategory(true);
      try {
        console.log('🔍 Sending to AI:', description); // Debug
        
        const response = await fetch('http://localhost:5000/api/expenses/categorize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({ description })
        });
        
        if (response.ok) {
          const data = await response.json();
          console.log('🎯 AI Response:', data); // Debug
          setSuggestedCategory(data.suggested_category);
          
          // ALWAYS auto-fill category with latest AI suggestion
          console.log('✅ Auto-updating category to:', data.suggested_category); // Debug
          setFormData(prev => ({ 
            ...prev, 
            category: data.suggested_category 
          }));
          
        } else {
          console.error('❌ API Error:', response.status);
        }
      } catch (error) {
        console.error('❌ Request failed:', error);
      } finally {
        setLoadingCategory(false);
      }
    } else {
      // Clear suggestions and reset category for short descriptions
      setSuggestedCategory('');
      setFormData(prev => ({ ...prev, category: '' }));
    }
  };

  return (
    <div>
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Expenses</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-500">
              Today (PST): {getTodayPST()}
            </span>
            <button
              onClick={() => setShowForm(true)}
              className="btn-primary"
            >
              Add Expense
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Add/Edit Form */}
        {showForm && (
          <div className="card mb-8">
            <h2 className="text-xl font-semibold mb-4">
              {editingExpense ? 'Edit Expense' : 'Add New Expense'}
            </h2>
            <form onSubmit={handleSubmit}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="form-label">Amount</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    required
                    className="form-input"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                    placeholder="0.00"
                  />
                </div>
                
                {/* Category moved to top right */}
                <div>
                  <label className="form-label">Category</label>
                  <select
                    required
                    className="form-input"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  >
                    <option value="">Select a category</option>
                    {categories.map((category) => (
                      <option key={category} value={category}>
                        {category}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Description moved to bottom left */}
                <div>
                  <label className="form-label">Description</label>
                  <div className="relative">
                    <input
                      type="text"
                      required
                      className="form-input"
                      value={formData.description}
                      onChange={(e) => handleDescriptionChange(e.target.value)}
                      placeholder="e.g., Starbucks coffee"
                    />
                    {loadingCategory && (
                      <div className="absolute right-2 top-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                      </div>
                    )}
                  </div>
                  {suggestedCategory && (
                    <p className="text-sm text-blue-600 mt-1">
                      💡 AI suggested: {suggestedCategory}
                    </p>
                  )}
                </div>

                <div>
                  <label className="form-label">Date (PST)</label>
                  <input
                    type="date"
                    required
                    className="form-input"
                    value={formData.date}
                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  />
                </div>
              </div>
              <div className="flex space-x-4 mt-6">
                <button type="submit" className="btn-primary">
                  {editingExpense ? 'Update Expense' : 'Add Expense'}
                </button>
                <button type="button" onClick={handleCancel} className="btn-secondary">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Expenses List */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
          </div>
        ) : expenses.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No expenses recorded yet.</p>
            <p className="text-gray-400">Add your first expense to get started!</p>
          </div>
        ) : (
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date (PST)
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {expenses.map((expense) => (
                  <tr key={expense.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDatePST(expense.date)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {expense.description}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                        {expense.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      ${expense.amount.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        onClick={() => handleEdit(expense)}
                        className="text-blue-600 hover:text-blue-900 mr-4"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(expense.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Expenses;
