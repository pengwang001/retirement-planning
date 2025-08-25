import React from 'react';

const SimulationSettingsForm = ({ formData, setFormData }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="form-section">
      <h2>Simulation Settings</h2>
      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="marketProfile">Market Return Assumptions</label>
          <select
            id="marketProfile"
            name="marketProfile"
            value={formData.marketProfile}
            onChange={handleChange}
          >
            <option value="Conservative">Conservative (5% avg, 12% volatility)</option>
            <option value="Moderate">Moderate (7% avg, 15% volatility)</option>
            <option value="Aggressive">Aggressive (9% avg, 18% volatility)</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="calculationMethod">Calculation Method</label>
          <select
            id="calculationMethod"
            name="calculationMethod"
            value={formData.calculationMethod}
            onChange={handleChange}
          >
            <option value="deterministic">Deterministic Growth</option>
            <option value="monteCarlo">Monte Carlo Simulation</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="socialSecurityClaimAge">Social Security Claim Age</label>
          <select
            id="socialSecurityClaimAge"
            name="socialSecurityClaimAge"
            value={formData.socialSecurityClaimAge}
            onChange={handleChange}
          >
            <option value="62">Early (62) - 70% of FRA benefit</option>
            <option value="67">Full Retirement Age (67) - 100% of FRA benefit</option>
            <option value="70">Delayed (70) - 132% of FRA benefit</option>
          </select>
        </div>

        {formData.maritalStatus !== 'single' && (
          <div className="form-group">
            <label htmlFor="spouseSocialSecurityClaimAge">Spouse Social Security Claim Age</label>
            <select
              id="spouseSocialSecurityClaimAge"
              name="socialSecurityClaimAge"
              value={formData.spouse.socialSecurityClaimAge}
              onChange={(e) => {
                setFormData(prev => ({
                  ...prev,
                  spouse: {
                    ...prev.spouse,
                    socialSecurityClaimAge: e.target.value
                  }
                }));
              }}
            >
              <option value="62">Early (62) - 70% of FRA benefit</option>
              <option value="67">Full Retirement Age (67) - 100% of FRA benefit</option>
              <option value="70">Delayed (70) - 132% of FRA benefit</option>
            </select>
          </div>
        )}
      </div>
    </div>
  );
};

export default SimulationSettingsForm;
