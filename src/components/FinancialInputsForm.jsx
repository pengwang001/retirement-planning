import React from 'react';

const FinancialInputsForm = ({ formData, setFormData }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSpouseChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      spouse: {
        ...prev.spouse,
        [name]: value
      }
    }));
  };

  return (
    <div className="form-section">
      <h2>Financial Information</h2>
      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="liquidAssets">Current Liquid Assets (Stock Market)</label>
          <input
            type="number"
            id="liquidAssets"
            name="liquidAssets"
            value={formData.liquidAssets}
            onChange={handleChange}
            min="0"
            step="1000"
            placeholder="e.g., 500000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="realEstateCashflow">Real Estate Annual Net Cashflow</label>
          <input
            type="number"
            id="realEstateCashflow"
            name="realEstateCashflow"
            value={formData.realEstateCashflow}
            onChange={handleChange}
            step="1000"
            placeholder="e.g., 24000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="annualIncome">Current Annual Income</label>
          <input
            type="number"
            id="annualIncome"
            name="annualIncome"
            value={formData.annualIncome}
            onChange={handleChange}
            min="0"
            step="1000"
            placeholder="e.g., 80000"
          />
        </div>

        <div className="form-group">
          <label htmlFor="yearsWorked">Years Worked</label>
          <input
            type="number"
            id="yearsWorked"
            name="yearsWorked"
            value={formData.yearsWorked}
            onChange={handleChange}
            min="0"
            max="50"
            placeholder="e.g., 15"
          />
        </div>

        <div className="form-group">
          <label htmlFor="annualContribution">Annual Contributions Until Retirement</label>
          <input
            type="number"
            id="annualContribution"
            name="annualContribution"
            value={formData.annualContribution}
            onChange={handleChange}
            min="0"
            step="1000"
            placeholder="e.g., 20000"
          />
        </div>

        {formData.maritalStatus !== 'single' && formData.spouse.bothWorking === 'both' && (
          <>
            <div className="form-group">
              <label htmlFor="spouseAnnualIncome">Spouse Annual Income</label>
              <input
                type="number"
                id="spouseAnnualIncome"
                name="annualIncome"
                value={formData.spouse.annualIncome}
                onChange={handleSpouseChange}
                min="0"
                step="1000"
                placeholder="e.g., 75000"
              />
            </div>

            <div className="form-group">
              <label htmlFor="spouseYearsWorked">Spouse Years Worked</label>
              <input
                type="number"
                id="spouseYearsWorked"
                name="yearsWorked"
                value={formData.spouse.yearsWorked}
                onChange={handleSpouseChange}
                min="0"
                max="50"
                placeholder="e.g., 12"
              />
            </div>

            <div className="form-group">
              <label htmlFor="spouseAnnualContribution">Spouse Annual Contributions</label>
              <input
                type="number"
                id="spouseAnnualContribution"
                name="annualContribution"
                value={formData.spouse.annualContribution}
                onChange={handleSpouseChange}
                min="0"
                step="1000"
                placeholder="e.g., 18000"
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default FinancialInputsForm;
