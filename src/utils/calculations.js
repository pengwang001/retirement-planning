// Retirement calculation utilities

// Social Security benefit calculations
export const calculateSocialSecurityBenefit = (birthYear, annualIncome, yearsWorked, claimAge) => {
  const fra = 67; // Full Retirement Age for birth year >= 1960
  
  // Calculate FRA benefit (approximately 40% of average annual income)
  let fraBenefit = annualIncome * 0.4;
  
  // Adjust for years worked (assuming 35 years is full career)
  const yearsAdjustment = Math.min(yearsWorked / 35, 1);
  fraBenefit *= yearsAdjustment;
  
  // Adjust for early/late claiming
  let benefit;
  if (claimAge === 62) {
    benefit = fraBenefit * 0.7; // 70% of FRA benefit
  } else if (claimAge === 70) {
    benefit = fraBenefit * 1.32; // 132% of FRA benefit
  } else {
    // Linear interpolation for ages between 62 and 70
    const ageDiff = claimAge - 62;
    const benefitIncrease = (0.32 * ageDiff) / 8;
    benefit = fraBenefit * (0.7 + benefitIncrease);
  }
  
  return Math.round(benefit);
};

// Spousal benefit calculation
export const calculateSpousalBenefit = (workingSpouseBenefit, nonWorkingSpouseAge, workingSpouseAge) => {
  const fra = 67;
  
  // Spousal benefit is up to 50% of working spouse's FRA benefit
  let spousalBenefit = workingSpouseBenefit * 0.5;
  
  // Adjust for early claiming (spousal benefit doesn't increase with delayed retirement)
  if (nonWorkingSpouseAge < fra) {
    const reduction = (fra - nonWorkingSpouseAge) * 0.025; // 2.5% reduction per year
    spousalBenefit *= (1 - reduction);
  }
  
  return Math.round(spousalBenefit);
};

// Market return assumptions
export const MARKET_RETURNS = {
  Conservative: { mean: 0.05, stdDev: 0.12 },
  Moderate: { mean: 0.07, stdDev: 0.15 },
  Aggressive: { mean: 0.09, stdDev: 0.18 }
};

// Monte Carlo simulation for portfolio growth
export const monteCarloSimulation = (initialBalance, annualContribution, years, marketProfile) => {
  const { mean, stdDev } = MARKET_RETURNS[marketProfile];
  const results = [];
  
  for (let year = 0; year < years; year++) {
    // Generate random return for this year
    const randomReturn = mean + (Math.random() - 0.5) * 2 * stdDev;
    
    if (year === 0) {
      results.push({
        year: year + 1,
        balance: initialBalance * (1 + randomReturn) + annualContribution
      });
    } else {
      const previousBalance = results[year - 1].balance;
      results.push({
        year: year + 1,
        balance: previousBalance * (1 + randomReturn) + annualContribution
      });
    }
  }
  
  return results;
};

// Deterministic growth calculation
export const deterministicGrowth = (initialBalance, annualContribution, years, marketProfile) => {
  const { mean } = MARKET_RETURNS[marketProfile];
  const results = [];
  
  for (let year = 0; year < years; year++) {
    if (year === 0) {
      results.push({
        year: year + 1,
        balance: initialBalance * (1 + mean) + annualContribution
      });
    } else {
      const previousBalance = results[year - 1].balance;
      results.push({
        year: year + 1,
        balance: previousBalance * (1 + mean) + annualContribution
      });
    }
  }
  
  return results;
};

// Calculate safe withdrawal rate (4% rule)
export const calculateSafeWithdrawal = (portfolioBalance) => {
  return portfolioBalance * 0.04;
};

// Calculate sustainable spending based on portfolio and other income sources
export const calculateSustainableSpending = (portfolioBalance, realEstateIncome, socialSecurityIncome, expenses) => {
  const safeWithdrawal = calculateSafeWithdrawal(portfolioBalance);
  const totalIncome = safeWithdrawal + realEstateIncome + socialSecurityIncome;
  
  // Ensure spending doesn't exceed sustainable income
  return Math.min(totalIncome, expenses);
};

// Format currency
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

// Calculate years until retirement
export const calculateYearsToRetirement = (currentAge, retirementAge) => {
  return Math.max(0, retirementAge - currentAge);
};

// Calculate current age from birth year
export const calculateCurrentAge = (birthYear) => {
  const currentYear = new Date().getFullYear();
  return currentYear - birthYear;
};
