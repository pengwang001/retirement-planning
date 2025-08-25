import React from 'react';

const BudgetBreakdownForm = ({ formData, setFormData }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      budget: {
        ...prev.budget,
        [name]: value
      }
    }));
  };

  return (
    <div className="form-section">
      <h2>Retirement Budget Breakdown</h2>
      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="housing">Housing / Mortgage</label>
          <input
            type="number"
            id="housing"
            name="housing"
            value={formData.budget.housing}
            onChange={handleChange}
            min="0"
            step="1000"
            placeholder="e.g., 24000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="healthcare">Healthcare Premiums & Expenses</label>
          <input
            type="number"
            id="healthcare"
            name="healthcare"
            value={formData.budget.healthcare}
            onChange={handleChange}
            min="0"
            step="1000"
            placeholder="e.g., 12000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="foodLiving">Food & Living Expenses</label>
          <input
            type="number"
            id="foodLiving"
            name="foodLiving"
            value={formData.budget.foodLiving}
            onChange={handleChange}
            min="0"
            step="1000"
            placeholder="e.g., 18000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="travelLeisure">Travel / Leisure</label>
          <input
            type="number"
            id="travelLeisure"
            name="travelLeisure"
            value={formData.budget.travelLeisure}
            onChange={handleChange}
            min="0"
            step="1000"
            placeholder="e.g., 15000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="otherDiscretionary">Other Discretionary</label>
          <input
            type="number"
            id="otherDiscretionary"
            name="otherDiscretionary"
            value={formData.budget.otherDiscretionary}
            onChange={handleChange}
            min="0"
            step="1000"
            placeholder="e.g., 10000"
          />
        </div>
      </div>

      <div style={{ marginTop: '1rem', padding: '1rem', background: '#f8fafc', borderRadius: '6px' }}>
        <strong>Total Annual Budget: </strong>
        <span style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#0f172a' }}>
          ${(parseFloat(formData.budget.housing) + 
              parseFloat(formData.budget.healthcare) + 
              parseFloat(formData.budget.foodLiving) + 
              parseFloat(formData.budget.travelLeisure) + 
              parseFloat(formData.budget.otherDiscretionary)).toLocaleString()}
        </span>
      </div>
    </div>
  );
};

export default BudgetBreakdownForm;
