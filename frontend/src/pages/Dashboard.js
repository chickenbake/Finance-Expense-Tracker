import React, { useState, useEffect } from 'react';
import { Pie, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import Navbar from '../components/Navbar';
import { expenseService } from '../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [aiInsights, setAiInsights] = useState('');
  const [loadingInsights, setLoadingInsights] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
    fetchAIInsights();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const data = await expenseService.getDashboardSummary();
      setDashboardData(data);
    } catch (error) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAIInsights = async () => {
    try {
      setLoadingInsights(true);
      const response = await fetch('https://finance-expense-tracker-467666307950.us-central1.run.app/api', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setAiInsights(data.insights);
      }
    } catch (error) {
      console.error('Failed to fetch AI insights:', error);
    } finally {
      setLoadingInsights(false);
    }
  };

  const pieChartData = {
    labels: Object.keys(dashboardData?.category_breakdown || {}),
    datasets: [
      {
        data: Object.values(dashboardData?.category_breakdown || {}),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
          '#FF6384',
          '#C9CBCF',
        ],
        hoverBackgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
          '#FF6384',
          '#C9CBCF',
        ],
      },
    ],
  };

  const barChartData = {
    labels: Object.keys(dashboardData?.daily_spending || {}),
    datasets: [
      {
        label: 'Daily Spending',
        data: Object.values(dashboardData?.daily_spending || {}),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  const barOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return '$' + value.toFixed(2);
          },
        },
      },
    },
  };

  if (loading) {
    return (
      <div>
        <Navbar />
        <div className="flex justify-center items-center min-h-screen">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* AI Insights Card - NEW */}
        <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg shadow-lg p-6 mb-8 text-white">
          <div className="flex items-center mb-4">
            <div className="bg-white bg-opacity-20 rounded-full p-2 mr-3">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h2 className="text-xl font-semibold">💡 AI Budget Insights</h2>
          </div>
          
          {loadingInsights ? (
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              <span>Analyzing your spending patterns...</span>
            </div>
          ) : (
            <p className="text-lg leading-relaxed">{aiInsights || 'Start adding expenses to get personalized insights!'}</p>
          )}
          
          <button 
            onClick={fetchAIInsights}
            className="mt-4 bg-white bg-opacity-20 hover:bg-opacity-30 px-4 py-2 rounded-lg transition-all duration-200"
          >
            🔄 Refresh Insights
          </button>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">This Month's Total</h3>
            <p className="text-3xl font-bold text-blue-600">
              ${dashboardData?.total_current_month?.toFixed(2) || '0.00'}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Last 30 Days Total</h3>
            <p className="text-3xl font-bold text-green-600">
              ${dashboardData?.total_last_30_days?.toFixed(2) || '0.00'}
            </p>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Pie Chart */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Spending by Category (Current Month)
            </h2>
            {Object.keys(dashboardData?.category_breakdown || {}).length > 0 ? (
              <div className="h-80">
                <Pie data={pieChartData} options={chartOptions} />
              </div>
            ) : (
              <div className="flex items-center justify-center h-80 text-gray-500">
                No expenses recorded for this month
              </div>
            )}
          </div>

          {/* Bar Chart */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Daily Spending (Last 30 Days)
            </h2>
            {Object.keys(dashboardData?.daily_spending || {}).length > 0 ? (
              <div className="h-80">
                <Bar data={barChartData} options={barOptions} />
              </div>
            ) : (
              <div className="flex items-center justify-center h-80 text-gray-500">
                No expenses recorded in the last 30 days
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
