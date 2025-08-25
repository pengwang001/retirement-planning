import React, { useState } from 'react';
import PersonalInfoForm from './components/PersonalInfoForm';
import FinancialInputsForm from './components/FinancialInputsForm';
import SimulationSettingsForm from './components/SimulationSettingsForm';
import BudgetBreakdownForm from './components/BudgetBreakdownForm';
import ResultsDisplay from './components/ResultsDisplay';
import { 
  calculateSocialSecurityBenefit, 
  calculateSpousalBenefit,
  monteCarloSimulation,
  deterministicGrowth,
  calculateSafeWithdrawal,
  calculateSustainableSpending,
  calculateCurrentAge,
  calculateYearsToRetirement
} from './utils/calculations';

function App() {
  const [formData, setFormData] = useState({
    maritalStatus: 'single',
    birthYear: '',
    retirementAge: '',
    liquidAssets: '',
    realEstateCashflow: '',
    annualIncome: '',
    yearsWorked: '',
    annualContribution: '',
    marketProfile: 'Moderate',
    calculationMethod: 'deterministic',
    socialSecurityClaimAge: '67',
    spouse: {
      birthYear: '',
      retirementAge: '',
      bothWorking: 'both',
      annualIncome: '',
      yearsWorked: '',
      annualContribution: '',
      socialSecurityClaimAge: '67'
    },
    budget: {
      housing: '',
      healthcare: '',
      foodLiving: '',
      travelLeisure: '',
      otherDiscretionary: ''
    }
  });

  const [results, setResults] = useState(null);
  const [isCalculating, setIsCalculating] = useState(false);

  const calculateRetirement = () => {
    setIsCalculating(true);
    
    // Simulate calculation time
    setTimeout(() => {
      try {
        const currentAge = calculateCurrentAge(parseInt(formData.birthYear));
        const yearsToRetirement = calculateYearsToRetirement(currentAge, parseInt(formData.retirementAge));
        const retirementAge = parseInt(formData.retirementAge);
        
        // Calculate portfolio growth during working years
        let portfolioBalance = parseFloat(formData.liquidAssets);
        const annualContribution = parseFloat(formData.annualContribution) || 0;
        
        if (formData.calculationMethod === 'monteCarlo') {
          const growthResults = monteCarloSimulation(
            portfolioBalance, 
            annualContribution, 
            yearsToRetirement, 
            formData.marketProfile
          );
          portfolioBalance = growthResults[growthResults.length - 1]?.balance || portfolioBalance;
        } else {
          const growthResults = deterministicGrowth(
            portfolioBalance, 
            annualContribution, 
            yearsToRetirement, 
            formData.marketProfile
          );
          portfolioBalance = growthResults[growthResults.length - 1]?.balance || portfolioBalance;
        }

        // Calculate Social Security benefits
        let primarySocialSecurity = 0;
        let spousalSocialSecurity = 0;
        
        if (parseInt(formData.socialSecurityClaimAge) <= retirementAge) {
          primarySocialSecurity = calculateSocialSecurityBenefit(
            parseInt(formData.birthYear),
            parseFloat(formData.annualIncome),
            parseInt(formData.yearsWorked),
            parseInt(formData.socialSecurityClaimAge)
          );
        }

        if (formData.maritalStatus !== 'single') {
          if (formData.spouse.bothWorking === 'both') {
            // Both working - calculate separately
            if (parseInt(formData.spouse.socialSecurityClaimAge) <= parseInt(formData.spouse.retirementAge)) {
              spousalSocialSecurity = calculateSocialSecurityBenefit(
                parseInt(formData.spouse.birthYear),
                parseFloat(formData.spouse.annualIncome),
                parseInt(formData.spouse.yearsWorked),
                parseInt(formData.spouse.socialSecurityClaimAge)
              );
            }
          } else {
            // Only one working - calculate spousal benefit
            spousalSocialSecurity = calculateSpousalBenefit(
              primarySocialSecurity,
              parseInt(formData.spouse.birthYear),
              parseInt(formData.birthYear)
            );
          }
        }

        // Calculate total annual income
        const realEstateIncome = parseFloat(formData.realEstateCashflow) || 0;
        const totalSocialSecurity = primarySocialSecurity + spousalSocialSecurity;
        const safeWithdrawal = calculateSafeWithdrawal(portfolioBalance);
        const totalAnnualIncome = safeWithdrawal + realEstateIncome + totalSocialSecurity;

        // Calculate annual budget
        const annualBudget = Object.values(formData.budget).reduce((sum, value) => sum + (parseFloat(value) || 0), 0);
        const surplusDeficit = totalAnnualIncome - annualBudget;

        // Generate retirement forecast (30 years)
        const forecast = [];
        let currentPortfolio = portfolioBalance;
        
        for (let year = 0; year < 30; year++) {
          const age = retirementAge + year;
          const startingBalance = currentPortfolio;
          
          // Calculate investment gains (assuming same market profile)
          const { mean } = formData.marketProfile === 'Conservative' ? { mean: 0.05 } : 
                           formData.marketProfile === 'Moderate' ? { mean: 0.07 } : { mean: 0.09 };
          const investmentGains = startingBalance * mean;
          
          // Real estate income
          const realEstateCashflow = realEstateIncome;
          
          // Social Security (starts at claim age)
          let socialSecurity = 0;
          if (age >= parseInt(formData.socialSecurityClaimAge)) {
            socialSecurity += primarySocialSecurity;
          }
          if (age >= parseInt(formData.spouse.socialSecurityClaimAge) && formData.maritalStatus !== 'single') {
            socialSecurity += spousalSocialSecurity;
          }
          
          // Spending
          const spending = annualBudget;
          
          // Ending balance
          const endingBalance = startingBalance + investmentGains + realEstateCashflow + socialSecurity - spending;
          currentPortfolio = endingBalance;
          
          forecast.push({
            age,
            startingBalance: Math.round(startingBalance),
            investmentGains: Math.round(investmentGains),
            realEstateCashflow: Math.round(realEstateCashflow),
            socialSecurity: Math.round(socialSecurity),
            spending: Math.round(spending),
            endingBalance: Math.round(endingBalance)
          });
        }

        // Generate chart data
        const portfolioBalanceChart = forecast.map(year => ({
          year: year.age,
          balance: year.endingBalance
        }));

        const results = {
          forecast,
          summary: {
            portfolioAtRetirement: Math.round(portfolioBalance),
            safeAnnualWithdrawal: Math.round(safeWithdrawal),
            totalAnnualIncome: Math.round(totalAnnualIncome),
            annualBudget: Math.round(annualBudget),
            surplusDeficit: Math.round(surplusDeficit),
            safeSustainableSpending: Math.round(calculateSustainableSpending(
              portfolioBalance, 
              realEstateIncome, 
              totalSocialSecurity, 
              annualBudget
            ))
          },
          charts: {
            portfolioBalance: portfolioBalanceChart
          }
        };

        setResults(results);
      } catch (error) {
        console.error('Calculation error:', error);
        alert('An error occurred during calculation. Please check your inputs.');
      } finally {
        setIsCalculating(false);
      }
    }, 1000);
  };

  const resetForm = () => {
    setFormData({
      maritalStatus: 'single',
      birthYear: '',
      retirementAge: '',
      liquidAssets: '',
      realEstateCashflow: '',
      annualIncome: '',
      yearsWorked: '',
      annualContribution: '',
      marketProfile: 'Moderate',
      calculationMethod: 'deterministic',
      socialSecurityClaimAge: '67',
      spouse: {
        birthYear: '',
        retirementAge: '',
        bothWorking: 'both',
        annualIncome: '',
        yearsWorked: '',
        annualContribution: '',
        socialSecurityClaimAge: '67'
      },
      budget: {
        housing: '',
        healthcare: '',
        foodLiving: '',
        travelLeisure: '',
        otherDiscretionary: ''
      }
    });
    setResults(null);
  };

  const isFormValid = () => {
    const requiredFields = [
      formData.birthYear,
      formData.retirementAge,
      formData.liquidAssets,
      formData.annualIncome,
      formData.yearsWorked
    ];
    
    if (formData.maritalStatus !== 'single') {
      requiredFields.push(
        formData.spouse.birthYear,
        formData.spouse.retirementAge
      );
      
      if (formData.spouse.bothWorking === 'both') {
        requiredFields.push(
          formData.spouse.annualIncome,
          formData.spouse.yearsWorked
        );
      }
    }
    
    const budgetTotal = Object.values(formData.budget).reduce((sum, value) => sum + (parseFloat(value) || 0), 0);
    
    return requiredFields.every(field => field !== '') && budgetTotal > 0;
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Retirement Planning Calculator</h1>
        <p>Plan your retirement with comprehensive financial analysis and forecasting</p>
      </div>

      <PersonalInfoForm formData={formData} setFormData={setFormData} />
      <FinancialInputsForm formData={formData} setFormData={setFormData} />
      <SimulationSettingsForm formData={formData} setFormData={setFormData} />
      <BudgetBreakdownForm formData={formData} setFormData={setFormData} />

      <div className="form-section">
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button 
            className="btn" 
            onClick={calculateRetirement}
            disabled={!isFormValid() || isCalculating}
          >
            {isCalculating ? 'Calculating...' : 'Calculate Retirement Plan'}
          </button>
          <button 
            className="btn btn-secondary" 
            onClick={resetForm}
            disabled={isCalculating}
          >
            Reset Form
          </button>
        </div>
      </div>

      {results && <ResultsDisplay results={results} formData={formData} />}
    </div>
  );
}

export default App;
