import React from 'react';

const PersonalInfoForm = ({ formData, setFormData }) => {
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
      <h2>Personal Information</h2>
      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="maritalStatus">Marital Status</label>
          <select
            id="maritalStatus"
            name="maritalStatus"
            value={formData.maritalStatus}
            onChange={handleChange}
          >
            <option value="single">Single</option>
            <option value="married">Married</option>
            <option value="couple">Couple (Unmarried)</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="birthYear">Year of Birth</label>
          <input
            type="number"
            id="birthYear"
            name="birthYear"
            value={formData.birthYear}
            onChange={handleChange}
            min="1940"
            max="2010"
            placeholder="e.g., 1980"
          />
        </div>

        <div className="form-group">
          <label htmlFor="retirementAge">Desired Retirement Age</label>
          <input
            type="number"
            id="retirementAge"
            name="retirementAge"
            value={formData.retirementAge}
            onChange={handleChange}
            min="55"
            max="75"
            placeholder="e.g., 65"
          />
        </div>

        {formData.maritalStatus !== 'single' && (
          <>
            <div className="form-group">
              <label htmlFor="spouseBirthYear">Spouse Year of Birth</label>
              <input
                type="number"
                id="spouseBirthYear"
                name="birthYear"
                value={formData.spouse.birthYear}
                onChange={handleSpouseChange}
                min="1940"
                max="2010"
                placeholder="e.g., 1982"
              />
            </div>

            <div className="form-group">
              <label htmlFor="spouseRetirementAge">Spouse Retirement Age</label>
              <input
                type="number"
                id="spouseRetirementAge"
                name="retirementAge"
                value={formData.spouse.retirementAge}
                onChange={handleSpouseChange}
                min="55"
                max="75"
                placeholder="e.g., 65"
              />
            </div>

            <div className="form-group">
              <label htmlFor="bothWorking">Both Spouses Working?</label>
              <select
                id="bothWorking"
                name="bothWorking"
                value={formData.spouse.bothWorking}
                onChange={handleSpouseChange}
              >
                <option value="both">Both Working</option>
                <option value="one">Only One Working</option>
              </select>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default PersonalInfoForm;
