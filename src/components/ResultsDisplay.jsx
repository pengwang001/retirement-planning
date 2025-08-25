import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { formatCurrency } from '../utils/calculations';

const ResultsDisplay = ({ results, formData }) => {
  if (!results) return null;

  const { forecast, summary, charts } = results;

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const budgetData = [
    { name: 'Housing', value: parseFloat(formData.budget.housing) },
    { name: 'Healthcare', value: parseFloat(formData.budget.healthcare) },
    { name: 'Food & Living', value: parseFloat(formData.budget.foodLiving) },
    { name: 'Travel & Leisure', value: parseFloat(formData.budget.travelLeisure) },
    { name: 'Other', value: parseFloat(formData.budget.otherDiscretionary) }
  ].filter(item => item.value > 0);

  return (
    <div className="results-section">
      <h2>Retirement Forecast Results</h2>
      
      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="summary-card">
          <h3>Portfolio at Retirement</h3>
          <div className="value positive">
            {formatCurrency(summary.portfolioAtRetirement)}
          </div>
        </div>
        <div className="summary-card">
          <h3>Safe Annual Withdrawal</h3>
          <div className="value positive">
            {formatCurrency(summary.safeAnnualWithdrawal)}
          </div>
        </div>
        <div className="summary-card">
          <h3>Total Annual Income</h3>
          <div className="value positive">
            {formatCurrency(summary.totalAnnualIncome)}
          </div>
        </div>
        <div className="summary-card">
          <h3>Annual Budget</h3>
          <div className="value">
            {formatCurrency(summary.annualBudget)}
          </div>
        </div>
        <div className="summary-card">
          <h3>Surplus/Deficit</h3>
          <div className={`value ${summary.surplusDeficit >= 0 ? 'positive' : 'negative'}`}>
            {formatCurrency(summary.surplusDeficit)}
          </div>
        </div>
      </div>

      {/* Portfolio Balance Chart */}
      <div className="chart-container">
        <h3>Portfolio Balance Over Time</h3>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={charts.portfolioBalance}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`} />
            <Tooltip 
              formatter={(value) => [formatCurrency(value), 'Portfolio Balance']}
              labelFormatter={(label) => `Year ${label}`}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="balance" 
              stroke="#3b82f6" 
              strokeWidth={3}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Spending Breakdown Chart */}
      <div className="chart-container">
        <h3>Spending Breakdown by Category</h3>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={budgetData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={120}
              fill="#8884d8"
              dataKey="value"
            >
              {budgetData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => [formatCurrency(value), 'Amount']} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Annual Forecast Table */}
      <h3>Annual Forecast</h3>
      <div style={{ overflowX: 'auto' }}>
        <table className="forecast-table">
          <thead>
            <tr>
              <th>Age</th>
              <th>Starting Balance</th>
              <th>Investment Gains</th>
              <th>Real Estate Cashflow</th>
              <th>Social Security</th>
              <th>Spending</th>
              <th>Ending Balance</th>
            </tr>
          </thead>
          <tbody>
            {forecast.map((year, index) => (
              <tr key={index}>
                <td>{year.age}</td>
                <td>{formatCurrency(year.startingBalance)}</td>
                <td>{formatCurrency(year.investmentGains)}</td>
                <td>{formatCurrency(year.realEstateCashflow)}</td>
                <td>{formatCurrency(year.socialSecurity)}</td>
                <td>{formatCurrency(year.spending)}</td>
                <td>{formatCurrency(year.endingBalance)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Safe Sustainable Spending Estimate */}
      <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#f0f9ff', borderRadius: '8px', border: '1px solid #0ea5e9' }}>
        <h3 style={{ color: '#0c4a6e', marginBottom: '1rem' }}>Safe Sustainable Annual Spending Estimate</h3>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#0c4a6e' }}>
          {formatCurrency(summary.safeSustainableSpending)}
        </div>
        <p style={{ marginTop: '0.5rem', color: '#0369a1', fontSize: '0.9rem' }}>
          Based on 4% withdrawal rule, real estate income, and Social Security benefits
        </p>
      </div>
    </div>
  );
};

export default ResultsDisplay;
