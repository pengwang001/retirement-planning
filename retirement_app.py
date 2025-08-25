#!/usr/bin/env python3
"""
Retirement Planning Calculator
A comprehensive web application for retirement planning with advanced financial modeling.
"""

from flask import Flask, render_template_string, request, jsonify
import math
import random
import requests
import json
from datetime import datetime

app = Flask(__name__)

# Error handlers for production
@app.errorhandler(500)
def internal_error(error):
    return "Something went wrong. Please try again.", 500

@app.errorhandler(404)
def not_found_error(error):
    return "Page not found.", 404

# HTML template for the application
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retirement Planning Calculator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .header h1 {
            font-size: 2.5rem;
            color: #0f172a;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            font-size: 1.1rem;
            color: #64748b;
        }
        
        .form-section {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }
        
        .form-section h2 {
            color: #0f172a;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 0.5rem;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
        }
        
        .form-group label {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #374151;
        }
        
        .form-group input,
        .form-group select {
            padding: 0.75rem;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 1rem;
            transition: border-color 0.2s;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .btn {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .btn:hover {
            background: #2563eb;
        }
        
        .btn:disabled {
            background: #9ca3af;
            cursor: not-allowed;
        }
        
        .btn-secondary {
            background: #6b7280;
        }
        
        .btn-secondary:hover {
            background: #4b5563;
        }
        
        .profile-section {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 1.5rem;
        }
        
        .profile-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .profile-input {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 0.9rem;
        }
        
        .profile-actions {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .profile-message {
            margin-top: 1rem;
            padding: 0.75rem;
            border-radius: 4px;
            display: none;
            font-size: 0.9rem;
        }
        
        .results-section {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }
        
        .results-section h2 {
            color: #0f172a;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 0.5rem;
        }
        
        .forecast-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
            font-size: 0.9rem;
        }
        
        .forecast-table th,
        .forecast-table td {
            padding: 0.75rem;
            text-align: right;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .forecast-table th {
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
        }
        
        .forecast-table th:first-child,
        .forecast-table td:first-child {
            text-align: left;
        }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }
        
        .summary-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
        }
        
        .summary-card h3 {
            color: #64748b;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .summary-card .value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
        }
        
        .summary-card .positive {
            color: #059669;
        }
        
        .summary-card .negative {
            color: #dc2626;
        }
        
        .spouse-section {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
            background: #f8fafc;
        }
        
        .spouse-section h4 {
            margin-bottom: 1rem;
            color: #374151;
        }
        
        .error {
            color: #dc2626;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
        
        .success {
            color: #059669;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
        
        .chart-container {
            margin-top: 2rem;
            height: auto;
            min-height: 200px;
            background: #f8fafc;
            border-radius: 8px;
            padding: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid #e2e8f0;
        }
        
        /* Results Layout Improvements */
        #results {
            max-width: 100%;
            overflow-x: hidden;
        }
        
        #results .chart-container {
            break-inside: avoid;
            page-break-inside: avoid;
        }
        
        /* Responsive Grid Adjustments */
        @media (max-width: 768px) {
            #results [style*="grid-template-columns"] {
                grid-template-columns: 1fr !important;
            }
            
            #results .chart-container {
                margin-bottom: 1rem;
            }
        }
        
        .chart-placeholder {
            text-align: center;
            color: #64748b;
        }
        
        .chart-placeholder h3 {
            margin-bottom: 1rem;
            color: #374151;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .forecast-table {
                font-size: 0.8rem;
            }
            
            .forecast-table th,
            .forecast-table td {
                padding: 0.5rem 0.25rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Retirement Planning Calculator</h1>
            <p>Plan your retirement with comprehensive financial analysis and forecasting</p>
        </div>

        <!-- Test Cases Section -->
        <div class="form-section">
            <h2>Test Cases - Social Security Benefit Examples</h2>
            
            <!-- Spouse Retirement Age Explanation -->
            <div style="background-color: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem;">
                <h4 style="color: #92400e; margin-top: 0;">💡 Important: Social Security Claim Ages</h4>
                <p style="margin-bottom: 0.5rem; color: #92400e;"><strong>Both spouses specify their Social Security claim age in Simulation Settings!</strong></p>
                <p style="margin-bottom: 0; color: #92400e;">Even if your spouse doesn't work, they can still claim Social Security benefits based on your work record. The claim age determines when benefits start and affects the benefit amount.</p>
            </div>
            
            <!-- Maximum Benefit Information -->
            <div style="background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="color: #92400e; margin-bottom: 1rem;">⚠️ Important: Social Security Maximum Benefit Cap</h3>
                <p style="color: #92400e; margin-bottom: 0.5rem;"><strong>2024 Maximum Benefit at Full Retirement Age (67): $45,864/year</strong></p>
                <p style="color: #92400e; font-size: 0.9rem;">
                    Even if your income suggests a higher benefit, Social Security caps the maximum monthly benefit at $3,822 ($45,864/year) at FRA.
                    This cap applies to all calculations in this application.
                </p>
            </div>
            
            <div style="background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem;">
                <h3 style="color: #0c4a6e; margin-bottom: 1rem;">Case 1: Couple, Only One Spouse Working</h3>
                <p><strong>Worker:</strong> Birth year 1965, Income $100,000, Years worked 35, Retirement age 62</p>
                <p><strong>Spouse:</strong> Birth year 1967, Not working</p>
                <p><strong>Expected Results:</strong></p>
                <ul>
                    <li>Worker FRA benefit: $40,000/year (at age 67) - <em>Below max cap</em></li>
                    <li>Worker benefit at 62: $28,000/year (70% of FRA)</li>
                    <li>Spouse benefit at 62: $14,000/year (35% of worker's FRA)</li>
                    <li><strong>Total: $42,000/year starting at age 62</strong></li>
                </ul>
            </div>
            
            <div style="background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem;">
                <h3 style="color: #0c4a6e; margin-bottom: 1rem;">Case 2: Couple, Both Working</h3>
                <p><strong>Spouse A:</strong> Birth year 1965, Income $100,000, Years worked 35, Retirement age 67</p>
                <p><strong>Spouse B:</strong> Birth year 1967, Income $60,000, Years worked 35, Retirement age 67</p>
                <p><strong>Expected Results:</strong></p>
                <ul>
                    <li>Spouse A benefit: $40,000/year (at FRA 67) - <em>Below max cap</em></li>
                    <li>Spouse B benefit: $24,000/year (at FRA 67)</li>
                    <li><strong>Total: $64,000/year starting at age 67</strong></li>
                </ul>
            </div>
            
            <div style="background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 8px; padding: 1.5rem;">
                <h3 style="color: #0c4a6e; margin-bottom: 1rem;">Case 3: High-Income Worker (Above Max Cap)</h3>
                <p><strong>Worker:</strong> Birth year 1965, Income $200,000, Years worked 35, Retirement age 67</p>
                <p><strong>Expected Results:</strong></p>
                <ul>
                    <li>Calculated FRA benefit: $80,000/year (40% of $200,000)</li>
                    <li><strong>Actual FRA benefit: $45,864/year (capped at maximum)</strong></li>
                    <li>Early claim at 62: $32,105/year (70% of capped amount)</li>
                </ul>
            </div>
        </div>

        <form method="POST" action="/calculate">
            <!-- Personal Information -->
            <div class="form-section">
                <h2>Personal Information</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="maritalStatus">Marital Status</label>
                        <select id="maritalStatus" name="maritalStatus" onchange="toggleSpouseFields()">
                            <option value="single">Single</option>
                            <option value="married">Married</option>
                            <option value="couple">Couple (Unmarried)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="birthYear">Year of Birth</label>
                        <input type="number" id="birthYear" name="birthYear" min="1940" max="2010" placeholder="e.g., 1980" required>
                    </div>

                    <div class="form-group">
                        <label for="retirementAge">Desired Retirement Age</label>
                        <input type="number" id="retirementAge" name="retirementAge" min="55" max="75" placeholder="e.g., 65" required>
                    </div>

                    <div class="form-group" id="spouseFields" style="display: none;">
                        <label for="spouseBirthYear">Spouse Year of Birth</label>
                        <input type="number" id="spouseBirthYear" name="spouseBirthYear" min="1940" max="2010" placeholder="e.g., 1982">
                    </div>



                    <div class="form-group" id="bothWorkingFields" style="display: none;">
                        <label for="bothWorking">Both Spouses Working?</label>
                        <select id="bothWorking" name="bothWorking" onchange="toggleSpouseFinancialFields()">
                            <option value="both">Both Working</option>
                            <option value="one">Only One Working</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Financial Information -->
            <div class="form-section">
                <h2>Financial Information</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="liquidAssets">Current Liquid Assets (Stock Market)</label>
                        <input type="number" id="liquidAssets" name="liquidAssets" min="0" step="1000" placeholder="e.g., 500000" required>
                    </div>

                    <div class="form-group">
                        <label for="realEstateCashflow">Real Estate Annual Net Cashflow</label>
                        <input type="number" id="realEstateCashflow" name="realEstateCashflow" step="1000" placeholder="e.g., 24000">
                    </div>

                    <div class="form-group">
                        <label for="annualIncome">Current Annual Income</label>
                        <input type="number" id="annualIncome" name="annualIncome" min="0" step="1000" placeholder="e.g., 80000" required>
                    </div>

                    <div class="form-group">
                        <label for="yearsWorked">Years Worked</label>
                        <input type="number" id="yearsWorked" name="yearsWorked" min="0" max="50" placeholder="e.g., 15" required>
                    </div>

                    <div class="form-group">
                        <label for="annualContribution">Annual Contributions Until Retirement</label>
                        <input type="number" id="annualContribution" name="annualContribution" min="0" step="1000" placeholder="e.g., 20000">
                    </div>

                    <div class="form-group" id="spouseIncomeFields" style="display: none;">
                        <label for="spouseAnnualIncome">Spouse Annual Income</label>
                        <input type="number" id="spouseAnnualIncome" name="spouseAnnualIncome" min="0" step="1000" placeholder="e.g., 75000">
                    </div>

                    <div class="form-group" id="spouseYearsFields" style="display: none;">
                        <label for="spouseYearsWorked">Spouse Years Worked</label>
                        <input type="number" id="spouseYearsWorked" name="spouseYearsWorked" min="0" max="50" placeholder="e.g., 12">
                    </div>

                    <div class="form-group" id="spouseContributionFields" style="display: none;">
                        <label for="spouseAnnualContribution">Spouse Annual Contributions</label>
                        <input type="number" id="spouseAnnualContribution" name="spouseAnnualContribution" min="0" step="1000" placeholder="e.g., 18000">
                    </div>
                </div>
            </div>

            <!-- Simulation Settings -->
            <div class="form-section">
                <h2>Simulation Settings</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="marketProfile">Market Return Assumptions</label>
                        <select id="marketProfile" name="marketProfile">
                            <option value="Conservative">Conservative (5% avg, 12% volatility)</option>
                            <option value="Moderate" selected>Moderate (7% avg, 15% volatility)</option>
                            <option value="Aggressive">Aggressive (9% avg, 18% volatility)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="calculationMethod">Calculation Method</label>
                        <select id="calculationMethod" name="calculationMethod">
                            <option value="deterministic" selected>Deterministic Growth</option>
                            <option value="monteCarlo">Monte Carlo Simulation</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="socialSecurityClaimAge">Social Security Claim Age</label>
                        <select id="socialSecurityClaimAge" name="socialSecurityClaimAge">
                            <option value="62">Early (62) - 70% of FRA benefit</option>
                            <option value="67" selected>Full Retirement Age (67) - 100% of FRA benefit</option>
                            <option value="70">Delayed (70) - 132% of FRA benefit</option>
                        </select>
                    </div>

                    <div class="form-group" id="spouseSSFields" style="display: none;">
                        <label for="spouseSocialSecurityClaimAge">Spouse Social Security Claim Age</label>
                        <select id="spouseSocialSecurityClaimAge" name="spouseSocialSecurityClaimAge">
                            <option value="62">Early (62) - 70% of FRA benefit</option>
                            <option value="67" selected>Full Retirement Age (67) - 100% of FRA benefit</option>
                            <option value="70">Delayed (70) - 132% of FRA benefit</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Budget Breakdown -->
            <div class="form-section">
                <h2>Retirement Budget Breakdown</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="housing">Housing / Mortgage</label>
                        <input type="number" id="housing" name="housing" min="0" step="1000" placeholder="e.g., 24000" required>
                    </div>

                    <div class="form-group">
                        <label for="state">State</label>
                        <select id="state" name="state" required>
                            <option value="">Select State</option>
                            <option value="AL">Alabama</option>
                            <option value="AK">Alaska</option>
                            <option value="AZ">Arizona</option>
                            <option value="AR">Arkansas</option>
                            <option value="CA">California</option>
                            <option value="CO">Colorado</option>
                            <option value="CT">Connecticut</option>
                            <option value="DE">Delaware</option>
                            <option value="FL">Florida</option>
                            <option value="GA">Georgia</option>
                            <option value="HI">Hawaii</option>
                            <option value="ID">Idaho</option>
                            <option value="IL">Illinois</option>
                            <option value="IN">Indiana</option>
                            <option value="IA">Iowa</option>
                            <option value="KS">Kansas</option>
                            <option value="KY">Kentucky</option>
                            <option value="LA">Louisiana</option>
                            <option value="ME">Maine</option>
                            <option value="MD">Maryland</option>
                            <option value="MA">Massachusetts</option>
                            <option value="MI">Michigan</option>
                            <option value="MN">Minnesota</option>
                            <option value="MS">Mississippi</option>
                            <option value="MO">Missouri</option>
                            <option value="MT">Montana</option>
                            <option value="NE">Nebraska</option>
                            <option value="NV">Nevada</option>
                            <option value="NH">New Hampshire</option>
                            <option value="NJ">New Jersey</option>
                            <option value="NM">New Mexico</option>
                            <option value="NY">New York</option>
                            <option value="NC">North Carolina</option>
                            <option value="ND">North Dakota</option>
                            <option value="OH">Ohio</option>
                            <option value="OK">Oklahoma</option>
                            <option value="OR">Oregon</option>
                            <option value="PA">Pennsylvania</option>
                            <option value="RI">Rhode Island</option>
                            <option value="SC">South Carolina</option>
                            <option value="SD">South Dakota</option>
                            <option value="TN">Tennessee</option>
                            <option value="TX">Texas</option>
                            <option value="UT">Utah</option>
                            <option value="VT">Vermont</option>
                            <option value="VA">Virginia</option>
                            <option value="WA">Washington</option>
                            <option value="WV">West Virginia</option>
                            <option value="WI">Wisconsin</option>
                            <option value="WY">Wyoming</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="zipCode">ZIP Code</label>
                        <input type="text" id="zipCode" name="zipCode" pattern="[0-9]{5}" placeholder="e.g., 12345" required>
                    </div>

                    <div class="form-group">
                        <label for="tobaccoUse">Tobacco Use</label>
                        <select id="tobaccoUse" name="tobaccoUse">
                            <option value="false">No</option>
                            <option value="true">Yes</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="healthcare">Healthcare Premiums & Expenses (Both Spouses)</label>
                        <input type="number" id="healthcare" name="healthcare" min="0" step="1000" placeholder="Auto-estimated for both spouses" readonly>
                        <small style="color: #6b7280; font-size: 0.875rem;">
                            Premium auto-estimated for both spouses at retirement age using CMS Marketplace API data based on age, income, state, ZIP code, and tobacco use
                        </small>
                    </div>

                    <div class="form-group">
                        <label for="foodLiving">Food & Living Expenses</label>
                        <input type="number" id="foodLiving" name="foodLiving" min="0" step="1000" placeholder="e.g., 18000" required>
                    </div>

                    <div class="form-group">
                        <label for="travelLeisure">Travel / Leisure</label>
                        <input type="number" id="travelLeisure" name="travelLeisure" min="0" step="1000" placeholder="e.g., 15000" required>
                    </div>

                    <div class="form-group">
                        <label for="otherDiscretionary">Other Discretionary</label>
                        <input type="number" id="otherDiscretionary" name="otherDiscretionary" min="0" step="1000" placeholder="e.g., 10000" required>
                    </div>
                </div>

                <div style="margin-top: 1rem; padding: 1rem; background: #f8fafc; border-radius: 6px;">
                    <strong>Total Annual Budget: </strong>
                    <span id="totalBudget" style="font-size: 1.2rem; font-weight: bold; color: #0f172a;">$0</span>
                </div>
            </div>

            <div class="form-section">
                <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                    <button type="submit" class="btn">Calculate Retirement Plan</button>
                    <button type="button" class="btn btn-secondary" onclick="resetForm()">Reset Form</button>
                    <button type="button" class="btn btn-secondary" onclick="saveProfile()">Save Profile</button>
                    <button type="button" class="btn btn-secondary" onclick="loadProfile()">Load Profile</button>
                </div>
                
                <!-- Profile Management Section -->
                <div class="profile-section">
                    <h4 style="margin-top: 0; color: #374151;">Profile Management</h4>
                    <div class="profile-grid">
                        <div>
                            <label for="profileName" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #374151;">Profile Name:</label>
                            <input type="text" id="profileName" class="profile-input" placeholder="e.g., Default, Conservative, Aggressive">
                        </div>
                        <div>
                            <label for="profileAction" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #374151;">Action:</label>
                            <select id="profileAction" class="profile-input">
                                <option value="save">Save Current Profile</option>
                                <option value="load">Load Selected Profile</option>
                                <option value="delete">Delete Selected Profile</option>
                            </select>
                        </div>
                        <div>
                            <label for="profileSelect" style="display: block; margin-bottom: 0.5rem; font-weight: 600; color: #374151;">Select Profile:</label>
                            <select id="profileSelect" class="profile-input">
                                <option value="">No profiles saved</option>
                            </select>
                        </div>
                    </div>
                    <div class="profile-actions">
                        <button type="button" class="btn btn-secondary" onclick="executeProfileAction()" style="font-size: 0.9rem;">Execute Action</button>
                        <button type="button" class="btn btn-secondary" onclick="exportProfiles()" style="font-size: 0.9rem;">Export All Profiles</button>
                        <button type="button" class="btn btn-secondary" onclick="importProfiles()" style="font-size: 0.9rem;">Import Profiles</button>
                    </div>
                    <div id="profileMessage" class="profile-message"></div>
                </div>
            </div>
        </form>

        {% if results %}
        <div class="results-section">
            <h2>Retirement Forecast Results</h2>
            
            <!-- Summary Cards -->
            <div class="summary-cards">
                <div class="summary-card">
                    <h3>Portfolio at Retirement</h3>
                    <div class="value positive">${{ "{:,.0f}".format(results.summary.portfolioAtRetirement) }}</div>
                </div>
                <div class="summary-card">
                    <h3>Safe Annual Withdrawal</h3>
                    <div class="value positive">${{ "{:,.0f}".format(results.summary.safeAnnualWithdrawal) }}</div>
                </div>
                <div class="summary-card">
                    <h3>Total Annual Income</h3>
                    <div class="value positive">${{ "{:,.0f}".format(results.summary.totalAnnualIncome) }}</div>
                </div>
                <div class="summary-card">
                    <h3>Annual Budget</h3>
                    <div class="value">${{ "{:,.0f}".format(results.summary.annualBudget) }}</div>
                </div>
                <div class="summary-card">
                    <h3>Surplus/Deficit</h3>
                    <div class="value {{ 'positive' if results.summary.surplusDeficit >= 0 else 'negative' }}">
                        ${{ "{:,.0f}".format(results.summary.surplusDeficit) }}
                    </div>
                </div>
            </div>

            <!-- Results Grid Layout - First Row -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 2.5rem; margin-bottom: 3rem;">
                
                <!-- Portfolio Balance Chart -->
                <div style="background: #ffffff; padding: 2rem; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: fit-content;">
                    <h3 style="margin-top: 0; color: #1e40af; font-size: 1.25rem;">Portfolio Balance Over Time</h3>
                    <p style="color: #475569; margin-bottom: 1.5rem;">Portfolio balance projection from current age ({{ results.forecast[0].age }}) through retirement to age {{ results.forecast[-1].age }}</p>
                    <div style="display: grid; grid-template-columns: 1fr; gap: 1rem;">
                        <div style="padding: 1rem; background: #f8fafc; border-radius: 8px; border-left: 4px solid #3b82f6;">
                            <p style="margin: 0; font-weight: 600;"><strong>Working Years:</strong><br>${{ "{:,.0f}".format(results.forecast[0].startingBalance) }} → ${{ "{:,.0f}".format(results.forecast[results.yearsToRetirement].endingBalance) }}</p>
                        </div>
                        <div style="padding: 1rem; background: #f8fafc; border-radius: 8px; border-left: 4px solid #10b981;">
                            <p style="margin: 0; font-weight: 600;"><strong>Retirement Years:</strong><br>${{ "{:,.0f}".format(results.forecast[results.yearsToRetirement + 1].startingBalance) }} → ${{ "{:,.0f}".format(results.forecast[-1].endingBalance) }}</p>
                        </div>
                        <div style="padding: 1rem; background: #fef3c7; border-radius: 8px; border-left: 4px solid #f59e0b;">
                            <p style="margin: 0; font-weight: 600;"><strong>Peak Portfolio Value:</strong><br>${{ "{:,.0f}".format(results.forecast|max(attribute='endingBalance')|attr('endingBalance') or 0) }}</p>
                        </div>
                        <div style="padding: 1rem; background: #f0f9ff; border-radius: 8px; border-left: 4px solid #0ea5e9;">
                            <p style="margin: 0; font-weight: 600;"><strong>Total Growth Period:</strong><br>{{ results.forecast[-1].year - results.forecast[0].year }} years</p>
                        </div>
                    </div>
                </div>

                <!-- Spending Breakdown Chart -->
                <div style="background: #ffffff; padding: 2rem; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: fit-content;">
                    <h3 style="margin-top: 0; color: #1e40af; font-size: 1.25rem;">Spending Breakdown by Category</h3>
                    <div style="display: grid; grid-template-columns: 1fr; gap: 1rem;">
                        <div style="padding: 1rem; background: #fef2f2; border-radius: 8px; border-left: 4px solid #ef4444;">
                            <p style="margin: 0; font-weight: 600;"><strong>Housing:</strong> ${{ "{:,.0f}".format(results.budget.housing) }} <span style="color: #6b7280; font-weight: normal;">({{ "%.1f".format(results.budget.housing / results.summary.annualBudget * 100) if results.summary.annualBudget > 0 else 0 }}%)</span></p>
                        </div>
                        <div style="padding: 1rem; background: #f0f9ff; border-radius: 8px; border-left: 4px solid #0ea5e9;">
                            <p style="margin: 0; font-weight: 600;"><strong>Healthcare:</strong> ${{ "{:,.0f}".format(results.budget.healthcare) }} <span style="color: #6b7280; font-weight: normal;">({{ "%.1f".format(results.budget.healthcare / results.summary.annualBudget * 100) if results.summary.annualBudget > 0 else 0 }}%)</span></p>
                        </div>
                        <div style="padding: 1rem; background: #f0fdf4; border-radius: 8px; border-left: 4px solid #22c55e;">
                            <p style="margin: 0; font-weight: 600;"><strong>Food & Living:</strong> ${{ "{:,.0f}".format(results.budget.foodLiving) }} <span style="color: #6b7280; font-weight: normal;">({{ "%.1f".format(results.budget.foodLiving / results.summary.annualBudget * 100) if results.summary.annualBudget > 0 else 0 }}%)</span></p>
                        </div>
                        <div style="padding: 1rem; background: #fefce8; border-radius: 8px; border-left: 4px solid #eab308;">
                            <p style="margin: 0; font-weight: 600;"><strong>Travel & Leisure:</strong> ${{ "{:,.0f}".format(results.budget.travelLeisure) }} <span style="color: #6b7280; font-weight: normal;">({{ "%.1f".format(results.budget.travelLeisure / results.summary.annualBudget * 100) if results.summary.annualBudget > 0 else 0 }}%)</span></p>
                        </div>
                        <div style="padding: 1rem; background: #f3f4f6; border-radius: 8px; border-left: 4px solid #6b7280;">
                            <p style="margin: 0; font-weight: 600;"><strong>Other:</strong> ${{ "{:,.0f}".format(results.budget.otherDiscretionary) }} <span style="color: #6b7280; font-weight: normal;">({{ "%.1f".format(results.budget.otherDiscretionary / results.summary.annualBudget * 100) if results.summary.annualBudget > 0 else 0 }}%)</span></p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Extended Asset Growth Chart to Age 100 -->
            <div style="background: #ffffff; padding: 2rem; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 3rem;">
                <h3 style="margin-top: 0; color: #1e40af; font-size: 1.25rem;">Total Asset Growth: Current Age to 100</h3>
                {% if results.extendedAssetChart and results.extendedAssetChart|length > 0 %}
                    <p style="color: #475569; margin-bottom: 1.5rem;">Long-term projection showing total asset value growth from age {{ results.extendedAssetChart[0].age }} to age 100</p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
                        <div style="padding: 1.5rem; background: #f0fdf4; border-radius: 8px; border-left: 4px solid #22c55e;">
                            <p style="margin: 0; font-weight: 600;"><strong>Current Assets:</strong><br><span style="font-size: 1.1rem; color: #166534;">${{ "{:,.0f}".format(results.extendedAssetChart[0].totalAssets) }}</span></p>
                        </div>
                        <div style="padding: 1.5rem; background: #fef3c7; border-radius: 8px; border-left: 4px solid #f59e0b;">
                            <p style="margin: 0; font-weight: 600;"><strong>Peak Assets:</strong><br><span style="font-size: 1.1rem; color: #92400e;">
                                {% set peak_assets = results.extendedAssetChart|max(attribute='totalAssets') %}
                                {% if peak_assets %}
                                    ${{ "{:,.0f}".format(peak_assets.totalAssets) }}
                                {% else %}
                                    $0
                                {% endif %}
                            </span></p>
                        </div>
                        <div style="padding: 1.5rem; background: #f0f9ff; border-radius: 8px; border-left: 4px solid #0ea5e9;">
                            <p style="margin: 0; font-weight: 600;"><strong>Assets at Age 100:</strong><br><span style="font-size: 1.1rem; color: #0369a1;">${{ "{:,.0f}".format(results.extendedAssetChart[-1].totalAssets) }}</span></p>
                        </div>
                        <div style="padding: 1.5rem; background: #f3f4f6; border-radius: 8px; border-left: 4px solid #6b7280;">
                            <p style="margin: 0; font-weight: 600;"><strong>Total Growth Period:</strong><br><span style="font-size: 1.1rem; color: #374151;">{{ results.extendedAssetChart[-1].year - results.extendedAssetChart[0].year }} years</span></p>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                        <p style="color: #6b7280; font-size: 0.9rem; margin: 0; padding: 0.75rem; background: #f9fafb; border-radius: 6px;">📊 Extended chart data: {{ results.extendedAssetChart|length }} data points</p>
                        <p style="color: #6b7280; font-size: 0.9rem; margin: 0; padding: 0.75rem; background: #f9fafb; border-radius: 6px;">📈 Sample values: Age 50: ${{ "{:,.0f}".format(results.extendedAssetChart[1].totalAssets) if results.extendedAssetChart|length > 1 else 'N/A' }}, Age 60: ${{ "{:,.0f}".format(results.extendedAssetChart[11].totalAssets) if results.extendedAssetChart|length > 11 else 'N/A' }}</p>
                    </div>
                
                    <!-- Key Milestones -->
                    <div style="margin-top: 1.5rem; padding: 1.5rem; background: #f0f9ff; border-radius: 8px; border: 1px solid #0ea5e9;">
                        <h4 style="margin-top: 0; color: #0369a1; font-size: 1.1rem;">🎯 Key Milestones</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; font-size: 0.95rem;">
                            <div style="padding: 1rem; background: #ffffff; border-radius: 6px; border: 1px solid #dbeafe;">
                                <strong style="color: #1e40af;">Retirement Age ({{ results.extendedAssetChart[results.yearsToRetirement].age }}):</strong><br>
                                <span style="font-size: 1.1rem; color: #1e40af;">${{ "{:,.0f}".format(results.extendedAssetChart[results.yearsToRetirement].totalAssets) }}</span>
                            </div>
                            <div style="padding: 1rem; background: #ffffff; border-radius: 6px; border: 1px solid #dbeafe;">
                                <strong style="color: #1e40af;">Age 70:</strong><br>
                                <span style="font-size: 1.1rem; color: #1e40af;">
                                    {% if results.yearsToRetirement + 5 < results.extendedAssetChart|length %}
                                        ${{ "{:,.0f}".format(results.extendedAssetChart[results.yearsToRetirement + 5].totalAssets) }}
                                    {% else %}
                                        N/A
                                    {% endif %}
                                </span>
                            </div>
                            <div style="padding: 1rem; background: #ffffff; border-radius: 6px; border: 1px solid #dbeafe;">
                                <strong style="color: #1e40af;">Age 80:</strong><br>
                                <span style="font-size: 1.1rem; color: #1e40af;">
                                    {% if results.yearsToRetirement + 15 < results.extendedAssetChart|length %}
                                        ${{ "{:,.0f}".format(results.extendedAssetChart[results.yearsToRetirement + 15].totalAssets) }}
                                    {% else %}
                                        N/A
                                    {% endif %}
                                </span>
                            </div>
                            <div style="padding: 1rem; background: #ffffff; border-radius: 6px; border: 1px solid #dbeafe;">
                                <strong style="color: #1e40af;">Age 90:</strong><br>
                                <span style="font-size: 1.1rem; color: #1e40af;">
                                    {% if results.yearsToRetirement + 25 < results.extendedAssetChart|length %}
                                        ${{ "{:,.0f}".format(results.extendedAssetChart[results.yearsToRetirement + 25].totalAssets) }}
                                    {% else %}
                                        N/A
                                    {% endif %}
                                </span>
                            </div>
                        </div>
                {% else %}
                    <p style="color: #6b7280;">Extended asset chart data not available</p>
                {% endif %}
            </div>

            <!-- Annual Forecast Table -->
            <h3>Comprehensive Financial Forecast</h3>
            <p style="color: #6b7280; margin-bottom: 1rem;">Forecast data: {{ results.forecast|length }} years</p>
            <div style="overflow-x: auto;">
                <table class="forecast-table">
                    <thead>
                        <tr>
                            <th>Year</th>
                            <th>Age</th>
                            <th>Period</th>
                            <th>Starting Balance</th>
                            <th>Investment Gains</th>
                            <th>Contributions</th>
                            <th>Real Estate CF</th>
                            <th>Social Security</th>
                            <th>Spending</th>
                            <th>Ending Balance</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for year in results.forecast %}
                        <tr style="background-color: {{ '#f8fafc' if year.period == 'Working' else 'white' }};">
                            <td>{{ year.year }}</td>
                            <td>{{ year.age }}</td>
                            <td>
                                <span style="padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600; 
                                           background-color: {{ '#dbeafe' if year.period == 'Working' else '#dcfce7' }};
                                           color: {{ '#1e40af' if year.period == 'Working' else '#166534' }};">
                                    {{ year.period }}
                                </span>
                            </td>
                            <td>${{ "{:,.0f}".format(year.startingBalance) }}</td>
                            <td>${{ "{:,.0f}".format(year.investmentGains) }}</td>
                            <td>${{ "{:,.0f}".format(year.contribution) }}</td>
                            <td>${{ "{:,.0f}".format(year.realEstateCashflow) }}</td>
                            <td>${{ "{:,.0f}".format(year.socialSecurity) }}</td>
                            <td>${{ "{:,.0f}".format(year.spending) }}</td>
                            <td>${{ "{:,.0f}".format(year.endingBalance) }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <div style="margin-top: 1rem; padding: 1rem; background: #f0f9ff; border-radius: 6px; border: 1px solid #0ea5e9;">
                <p style="margin: 0; color: #0369a1; font-size: 0.9rem;">
                    <strong>Legend:</strong> 
                    <span style="background: #dbeafe; color: #1e40af; padding: 0.2rem 0.4rem; border-radius: 3px; font-size: 0.8rem;">Working</span> = 
                    Accumulation phase with contributions, 
                    <span style="background: #dcfce7; color: #166534; padding: 0.2rem 0.4rem; border-radius: 3px; font-size: 0.8rem;">Retirement</span> = 
                    Distribution phase with Social Security and spending
                </p>
            </div>

            <!-- Second Row: Social Security and Safe Spending -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 3rem; margin-bottom: 3rem;">
                
                <!-- Social Security Validation -->
                <div style="background: #fef3c7; padding: 2rem; border-radius: 12px; border: 1px solid #f59e0b; box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: fit-content;">
                    <h3 style="color: #92400e; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.25rem;">Social Security Benefit Validation</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem;">
                        <div style="padding: 1rem; background: #ffffff; border-radius: 8px; border: 1px solid #fbbf24;">
                            <strong style="color: #92400e;">Primary Worker FRA Benefit (age 67):</strong><br>
                            <span style="font-size: 1.1rem; color: #92400e; font-weight: 600;">${{ "{:,.0f}".format(results.socialSecurityDetails.primaryFRA) }}/year</span>
                            {% if results.socialSecurityDetails.primaryFRA >= 45864 %}
                            <br><small style="color: #dc2626;">⚠️ Capped at maximum</small>
                            {% endif %}
                        </div>
                        <div style="padding: 1rem; background: #ffffff; border-radius: 8px; border: 1px solid #fbbf24;">
                            <strong style="color: #92400e;">Primary Worker Claimed Benefit:</strong><br>
                            <span style="font-size: 1.1rem; color: #92400e; font-weight: 600;">${{ "{:,.0f}".format(results.socialSecurityDetails.primaryClaimed) }}/year</span>
                        </div>
                        <div style="padding: 1rem; background: #ffffff; border-radius: 8px; border: 1px solid #fbbf24;">
                            <strong style="color: #92400e;">Spousal FRA Benefit (age 67):</strong><br>
                            <span style="font-size: 1.1rem; color: #92400e; font-weight: 600;">${{ "{:,.0f}".format(results.socialSecurityDetails.spousalFRA) }}/year</span>
                            {% if results.socialSecurityDetails.spousalFRA >= 22932 %}
                            <br><small style="color: #dc2626;">⚠️ Capped at maximum</small>
                            {% endif %}
                        </div>
                        <div style="padding: 1rem; background: #ffffff; border-radius: 8px; border: 1px solid #fbbf24;">
                            <strong style="color: #92400e;">Spousal Claimed Benefit:</strong><br>
                            <span style="font-size: 1.1rem; color: #92400e; font-weight: 600;">${{ "{:,.0f}".format(results.socialSecurityDetails.spousalClaimed) }}/year</span>
                        </div>
                    </div>
                    <div style="background: #ffffff; padding: 1.5rem; border-radius: 8px; border: 1px solid #fbbf24; margin-bottom: 1rem;">
                        <strong style="color: #92400e;">Total Social Security Benefits:</strong><br>
                        <span style="font-size: 1.3rem; font-weight: bold; color: #92400e;">
                            FRA (age 67): ${{ "{:,.0f}".format(results.socialSecurityDetails.totalFRA) }}/year<br>
                            Claimed: ${{ "{:,.0f}".format(results.socialSecurityDetails.totalClaimed) }}/year
                        </span>
                    </div>
                    <div style="padding: 1rem; background: #fef3c7; border-radius: 8px; border: 1px solid #f59e0b;">
                        <small style="color: #92400e;">
                            <strong>Note:</strong> 2024 maximum benefit at FRA is $45,864/year. Spousal benefits are capped at 50% of the maximum ($22,932/year).
                        </small>
                    </div>
                </div>

                <!-- Safe Sustainable Spending Estimate -->
                <div style="background: #f0f9ff; padding: 2rem; border-radius: 12px; border: 1px solid #0ea5e9; box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: fit-content;">
                    <h3 style="color: #0c4a6e; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.25rem;">Safe Sustainable Annual Spending Estimate</h3>
                    <div style="font-size: 2rem; font-weight: bold; color: #0c4a6e; text-align: center; margin-bottom: 1rem;">
                        ${{ "{:,.0f}".format(results.summary.safeSustainableSpending) }}
                    </div>
                    <p style="margin-top: 0.5rem; color: #0369a9; font-size: 1rem; text-align: center; margin-bottom: 1.5rem;">
                        Maximum annual spending based on 4% withdrawal rule, real estate income, and Social Security benefits
                    </p>
                    <div style="padding: 1.5rem; background: #ffffff; border-radius: 8px; border: 1px solid #0ea5e9;">
                        <strong style="color: #0c4a6e; font-size: 1.1rem;">Breakdown:</strong><br><br>
                        <div style="display: grid; grid-template-columns: 1fr; gap: 0.75rem;">
                            <div style="padding: 0.75rem; background: #f0f9ff; border-radius: 6px; border-left: 3px solid #0ea5e9;">
                                <strong>4% Portfolio Withdrawal:</strong> ${{ "{:,.0f}".format(results.summary.safeAnnualWithdrawal) }}/year
                            </div>
                            <div style="padding: 0.75rem; background: #f0f9ff; border-radius: 6px; border-left: 3px solid #0ea5e9;">
                                <strong>Real Estate Income:</strong> ${{ "{:,.0f}".format(results.realEstateCashflow) }}/year
                            </div>
                            <div style="padding: 0.75rem; background: #f0f9ff; border-radius: 6px; border-left: 3px solid #0ea5e9;">
                                <strong>Social Security Benefits:</strong> ${{ "{:,.0f}".format(results.socialSecurityDetails.totalClaimed) }}/year
                            </div>
                        </div>
                        <div style="margin-top: 1rem; padding: 1rem; background: #0ea5e9; border-radius: 6px; text-align: center;">
                            <strong style="color: #ffffff; font-size: 1.1rem;">Total Sustainable Income: ${{ "{:,.0f}".format(results.summary.safeSustainableSpending) }}/year</strong>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Third Row: Extended Asset Growth Summary -->
            {% if results.extendedAssetChart and results.extendedAssetChart|length > 0 %}
            <div style="background: #fefce8; border: 1px solid #eab308; border-radius: 12px; padding: 2rem; margin-bottom: 3rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <h3 style="color: #92400e; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.25rem;">Long-Term Asset Growth Insights (Current Age to 100)</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                    <div style="background: #ffffff; padding: 1.5rem; border-radius: 8px; border: 1px solid #fbbf24;">
                        <h4 style="color: #92400e; margin-top: 0; font-size: 1.1rem;">📈 Growth Trajectory</h4>
                        <div style="display: grid; grid-template-columns: 1fr; gap: 1rem;">
                            <div style="padding: 0.75rem; background: #fefce8; border-radius: 6px; border-left: 3px solid #eab308;">
                                <strong style="color: #92400e;">Current Assets:</strong><br>
                                <span style="font-size: 1.1rem; color: #92400e;">${{ "{:,.0f}".format(results.extendedAssetChart[0].totalAssets) }}</span>
                            </div>
                            <div style="padding: 0.75rem; background: #fefce8; border-radius: 6px; border-left: 3px solid #eab308;">
                                <strong style="color: #92400e;">Peak Assets:</strong><br>
                                <span style="font-size: 1.1rem; color: #92400e;">
                                    {% set peak_assets = results.extendedAssetChart|max(attribute='totalAssets') %}
                                    {% if peak_assets %}
                                        ${{ "{:,.0f}".format(peak_assets.totalAssets) }}
                                    {% else %}
                                        $0
                                    {% endif %}
                                </span>
                            </div>
                            <div style="padding: 0.75rem; background: #fefce8; border-radius: 6px; border-left: 3px solid #eab308;">
                                <strong style="color: #92400e;">Final Assets (Age 100):</strong><br>
                                <span style="font-size: 1.1rem; color: #92400e;">${{ "{:,.0f}".format(results.extendedAssetChart[-1].totalAssets) }}</span>
                            </div>
                        </div>
                    </div>
                    <div style="background: #ffffff; padding: 1.5rem; border-radius: 8px; border: 1px solid #fbbf24;">
                        <h4 style="color: #92400e; margin-top: 0; font-size: 1.1rem;">🎯 Key Milestones</h4>
                        <div style="display: grid; grid-template-columns: 1fr; gap: 1rem;">
                            <div style="padding: 0.75rem; background: #fefce8; border-radius: 6px; border-left: 3px solid #eab308;">
                                <strong style="color: #92400e;">Retirement (Age {{ results.extendedAssetChart[results.yearsToRetirement].age }}):</strong><br>
                                <span style="font-size: 1.1rem; color: #92400e;">${{ "{:,.0f}".format(results.extendedAssetChart[results.yearsToRetirement].totalAssets) }}</span>
                            </div>
                            <div style="padding: 0.75rem; background: #fefce8; border-radius: 6px; border-left: 3px solid #eab308;">
                                <strong style="color: #92400e;">Age 80:</strong><br>
                                <span style="font-size: 1.1rem; color: #92400e;">
                                    {% if results.yearsToRetirement + 15 < results.extendedAssetChart|length %}
                                        ${{ "{:,.0f}".format(results.extendedAssetChart[results.yearsToRetirement + 15].totalAssets) }}
                                    {% else %}
                                        N/A
                                    {% endif %}
                                </span>
                            </div>
                            <div style="padding: 0.75rem; background: #fefce8; border-radius: 6px; border-left: 3px solid #eab308;">
                                <strong style="color: #92400e;">Age 90:</strong><br>
                                <span style="font-size: 1.1rem; color: #92400e;">
                                    {% if results.yearsToRetirement + 25 < results.extendedAssetChart|length %}
                                        ${{ "{:,.0f}".format(results.extendedAssetChart[results.yearsToRetirement + 25].totalAssets) }}
                                    {% else %}
                                        N/A
                                    {% endif %}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div style="background: #ffffff; padding: 1.5rem; border-radius: 8px; border: 1px solid #fbbf24;">
                        <h4 style="color: #92400e; margin-top: 0; font-size: 1.1rem;">💡 Planning Insights</h4>
                        <div style="display: grid; grid-template-columns: 1fr; gap: 1rem;">
                            <div style="padding: 1rem; background: #fefce8; border-radius: 6px; border-left: 3px solid #eab308;">
                                <strong style="color: #92400e;">Working Years:</strong><br>
                                <span style="color: #92400e; font-size: 0.95rem;">Asset accumulation through contributions and investment growth</span>
                            </div>
                            <div style="padding: 1rem; background: #fefce8; border-radius: 6px; border-left: 3px solid #eab308;">
                                <strong style="color: #92400e;">Retirement Years:</strong><br>
                                <span style="color: #92400e; font-size: 0.95rem;">Asset distribution with Social Security and real estate income</span>
                            </div>
                            <div style="padding: 1rem; background: #fefce8; border-radius: 6px; border-left: 3px solid #eab308;">
                                <strong style="color: #92400e;">Longevity Planning:</strong><br>
                                <span style="color: #92400e; font-size: 0.95rem;">Assets projected to age 100 for comprehensive planning</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
        {% endif %}
    </div>

    <script>
        function toggleSpouseFields() {
            const maritalStatus = document.getElementById('maritalStatus').value;
            const spouseFields = document.getElementById('spouseFields');
            const bothWorkingFields = document.getElementById('bothWorkingFields');
            const spouseSSFields = document.getElementById('spouseSSFields');
            
            if (maritalStatus !== 'single') {
                spouseFields.style.display = 'block';
                bothWorkingFields.style.display = 'block';
                spouseSSFields.style.display = 'block';
            } else {
                spouseFields.style.display = 'none';
                bothWorkingFields.style.display = 'none';
                spouseSSFields.style.display = 'none';
                toggleSpouseFinancialFields();
            }
        }
        
        function toggleSpouseFinancialFields() {
            const bothWorking = document.getElementById('bothWorking').value;
            const spouseIncomeFields = document.getElementById('spouseIncomeFields');
            const spouseYearsFields = document.getElementById('spouseYearsFields');
            const spouseContributionFields = document.getElementById('spouseContributionFields');
            
            if (bothWorking === 'both') {
                spouseIncomeFields.style.display = 'block';
                spouseYearsFields.style.display = 'block';
                spouseContributionFields.style.display = 'block';
            } else {
                spouseIncomeFields.style.display = 'none';
                spouseYearsFields.style.display = 'none';
                spouseContributionFields.style.display = 'none';
            }
        }
        

        
        function resetForm() {
            document.querySelector('form').reset();
            toggleSpouseFields();
            updateTotalBudget();
        }
        
        function updateTotalBudget() {
            const housing = parseFloat(document.getElementById('housing').value) || 0;
            const healthcare = parseFloat(document.getElementById('healthcare').value) || 0;
            const foodLiving = parseFloat(document.getElementById('foodLiving').value) || 0;
            const travelLeisure = parseFloat(document.getElementById('travelLeisure').value) || 0;
            const otherDiscretionary = parseFloat(document.getElementById('otherDiscretionary').value) || 0;
            
            const total = housing + healthcare + foodLiving + travelLeisure + otherDiscretionary;
            document.getElementById('totalBudget').textContent = '$' + total.toLocaleString();
        }
        
        // Add event listeners for budget fields
        document.addEventListener('DOMContentLoaded', function() {
            const budgetFields = ['housing', 'healthcare', 'foodLiving', 'travelLeisure', 'otherDiscretionary'];
            budgetFields.forEach(field => {
                document.getElementById(field).addEventListener('input', updateTotalBudget);
            });
            
                    // Add event listeners for healthcare estimation
        const healthcareFields = ['birthYear', 'annualIncome', 'state', 'zipCode', 'tobaccoUse'];
        healthcareFields.forEach(field => {
            document.getElementById(field).addEventListener('change', estimateHealthcare);
        });
        
        toggleSpouseFields();
        loadProfileList(); // Load saved profiles on page load
    });
    
    // Profile Management Functions
    function saveProfile() {
        const profileName = document.getElementById('profileName').value.trim();
        if (!profileName) {
            showProfileMessage('Please enter a profile name', 'error');
            return;
        }
        
        const profileData = collectFormData();
        const profiles = getProfiles();
        profiles[profileName] = profileData;
        localStorage.setItem('retirementProfiles', JSON.stringify(profiles));
        
        showProfileMessage(`Profile "${profileName}" saved successfully!`, 'success');
        loadProfileList();
        document.getElementById('profileName').value = '';
    }
    
    function loadProfile() {
        const profileSelect = document.getElementById('profileSelect');
        const selectedProfile = profileSelect.value;
        
        if (!selectedProfile) {
            showProfileMessage('Please select a profile to load', 'error');
            return;
        }
        
        const profiles = getProfiles();
        const profileData = profiles[selectedProfile];
        
        if (profileData) {
            populateForm(profileData);
            showProfileMessage(`Profile "${selectedProfile}" loaded successfully!`, 'success');
        } else {
            showProfileMessage('Profile not found', 'error');
        }
    }
    
    function executeProfileAction() {
        const action = document.getElementById('profileAction').value;
        const profileSelect = document.getElementById('profileSelect');
        const selectedProfile = profileSelect.value;
        
        switch (action) {
            case 'save':
                saveProfile();
                break;
            case 'load':
                if (selectedProfile) {
                    loadProfile();
                } else {
                    showProfileMessage('Please select a profile to load', 'error');
                }
                break;
            case 'delete':
                if (selectedProfile) {
                    deleteProfile(selectedProfile);
                } else {
                    showProfileMessage('Please select a profile to delete', 'error');
                }
                break;
        }
    }
    
    function deleteProfile(profileName) {
        if (confirm(`Are you sure you want to delete profile "${profileName}"?`)) {
            const profiles = getProfiles();
            delete profiles[profileName];
            localStorage.setItem('retirementProfiles', JSON.stringify(profiles));
            
            showProfileMessage(`Profile "${profileName}" deleted successfully!`, 'success');
            loadProfileList();
        }
    }
    
    function exportProfiles() {
        const profiles = getProfiles();
        const dataStr = JSON.stringify(profiles, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = 'retirement_profiles.json';
        link.click();
        
        showProfileMessage('All profiles exported successfully!', 'success');
    }
    
    function importProfiles() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = function(e) {
            const file = e.target.files[0];
            const reader = new FileReader();
            
            reader.onload = function(e) {
                try {
                    const importedProfiles = JSON.parse(e.target.result);
                    const existingProfiles = getProfiles();
                    
                    // Merge profiles, with imported ones taking precedence
                    const mergedProfiles = { ...existingProfiles, ...importedProfiles };
                    localStorage.setItem('retirementProfiles', JSON.stringify(mergedProfiles));
                    
                    showProfileMessage('Profiles imported successfully!', 'success');
                    loadProfileList();
                } catch (error) {
                    showProfileMessage('Error importing profiles: Invalid file format', 'error');
                }
            };
            
            reader.readAsText(file);
        };
        
        input.click();
    }
    
    function collectFormData() {
        const form = document.querySelector('form');
        const formData = new FormData(form);
        const data = {};
        
        // Collect all form fields
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Add timestamp
        data.timestamp = new Date().toISOString();
        
        return data;
    }
    
    function populateForm(profileData) {
        const form = document.querySelector('form');
        
        // Populate all form fields
        for (let key in profileData) {
            if (profileData.hasOwnProperty(key) && key !== 'timestamp') {
                const field = form.querySelector(`[name="${key}"]`);
                if (field) {
                    if (field.type === 'checkbox') {
                        field.checked = profileData[key] === 'true';
                    } else {
                        field.value = profileData[key];
                    }
                }
            }
        }
        
        // Trigger necessary UI updates
        toggleSpouseFields();
        updateTotalBudget();
        
        // Trigger healthcare estimation if location fields are filled
        if (profileData.state && profileData.zipCode) {
            estimateHealthcare();
        }
    }
    
    function getProfiles() {
        const profiles = localStorage.getItem('retirementProfiles');
        return profiles ? JSON.parse(profiles) : {};
    }
    
    function loadProfileList() {
        const profileSelect = document.getElementById('profileSelect');
        const profiles = getProfiles();
        
        // Clear existing options
        profileSelect.innerHTML = '';
        
        if (Object.keys(profiles).length === 0) {
            profileSelect.innerHTML = '<option value="">No profiles saved</option>';
            return;
        }
        
        // Add profile options
        Object.keys(profiles).forEach(profileName => {
            const option = document.createElement('option');
            option.value = profileName;
            option.textContent = profileName;
            profileSelect.appendChild(option);
        });
    }
    
    function showProfileMessage(message, type) {
        const messageDiv = document.getElementById('profileMessage');
        messageDiv.textContent = message;
        messageDiv.style.display = 'block';
        
        // Set styling based on message type
        if (type === 'success') {
            messageDiv.style.backgroundColor = '#d1fae5';
            messageDiv.style.color = '#065f46';
            messageDiv.style.border = '1px solid #10b981';
        } else if (type === 'error') {
            messageDiv.style.backgroundColor = '#fee2e2';
            messageDiv.style.color = '#991b1b';
            messageDiv.style.border = '1px solid #ef4444';
        }
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
    
    function estimateHealthcare() {
            const birthYear = document.getElementById('birthYear').value;
            const annualIncome = document.getElementById('annualIncome').value;
            const state = document.getElementById('state').value;
            const zipCode = document.getElementById('zipCode').value;
            const tobaccoUse = document.getElementById('tobaccoUse').value;
            
            if (birthYear && annualIncome && state && zipCode) {
                const currentYear = new Date().getFullYear();
                const age = currentYear - parseInt(birthYear);
                
                // Make API call to estimate healthcare premiums
                fetch('/estimate_healthcare', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        age: age,
                        income: parseInt(annualIncome),
                        state: state,
                        zip_code: zipCode,
                        tobacco_use: tobaccoUse === 'true'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('healthcare').value = data.estimated_annual_cost;
                        updateTotalBudget();
                        
                        // Show premium breakdown
                        showHealthcareBreakdown(data);
                    }
                })
                .catch(error => {
                    console.error('Error estimating healthcare:', error);
                });
            }
        }
        
        function showHealthcareBreakdown(data) {
            // Create or update healthcare breakdown display
            let breakdownDiv = document.getElementById('healthcareBreakdown');
            if (!breakdownDiv) {
                breakdownDiv = document.createElement('div');
                breakdownDiv.id = 'healthcareBreakdown';
                breakdownDiv.style.cssText = 'margin-top: 1rem; padding: 1rem; background: #f0f9ff; border-radius: 6px; border: 1px solid #0ea5e9;';
                document.getElementById('healthcare').parentNode.appendChild(breakdownDiv);
            }
            
            breakdownDiv.innerHTML = `
                <h4 style="color: #0c4a6e; margin-bottom: 0.5rem;">Healthcare Premium Estimates</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.5rem; margin-bottom: 1rem;">
                    <div><strong>Bronze:</strong> $${data.premiums.Bronze.monthly}/mo</div>
                    <div><strong>Silver:</strong> $${data.premiums.Silver.monthly}/mo</div>
                    <div><strong>Gold:</strong> $${data.premiums.Gold.monthly}/mo</div>
                    <div><strong>Platinum:</strong> $${data.premiums.Platinum.monthly}/mo</div>
                </div>
                <div style="font-size: 0.9rem; color: #0369a1; margin-bottom: 0.5rem;">
                    <strong>Recommended:</strong> ${data.recommended_tier} Plan
                    ${data.subsidy_eligible ? `(Eligible for ${data.subsidy_percentage}% subsidy)` : ''}
                </div>
                <div style="font-size: 0.8rem; color: #6b7280; padding-top: 0.5rem; border-top: 1px solid #e2e8f0;">
                    <strong>Data Source:</strong> ${data.source || 'CMS Marketplace API'}
                </div>
            `;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/estimate_healthcare', methods=['POST'])
def estimate_healthcare():
    """API endpoint for healthcare premium estimation."""
    try:
        data = request.get_json()
        age = data.get('age')
        income = data.get('income')
        state = data.get('state')
        zip_code = data.get('zip_code')
        tobacco_use = data.get('tobacco_use', False)
        
        if not all([age, income, state, zip_code]):
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
        # Estimate healthcare premiums
        healthcare_estimate = estimate_healthcare_premiums(
            age=age,
            income=income,
            state=state,
            zip_code=zip_code,
            tobacco_use=tobacco_use
        )
        
        return jsonify({
            'success': True,
            'premiums': healthcare_estimate['premiums'],
            'out_of_pocket': healthcare_estimate['out_of_pocket'],
            'subsidy_eligible': healthcare_estimate['subsidy_eligible'],
            'subsidy_percentage': healthcare_estimate['subsidy_percentage'],
            'estimated_annual_cost': healthcare_estimate['estimated_annual_cost'],
            'recommended_tier': healthcare_estimate['recommended_tier']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get form data
        marital_status = request.form.get('maritalStatus')
        birth_year = int(request.form.get('birthYear'))
        retirement_age = int(request.form.get('retirementAge'))
        liquid_assets = float(request.form.get('liquidAssets'))
        real_estate_cashflow = float(request.form.get('realEstateCashflow') or 0)
        annual_income = float(request.form.get('annualIncome'))
        years_worked = int(request.form.get('yearsWorked'))
        annual_contribution = float(request.form.get('annualContribution') or 0)
        market_profile = request.form.get('marketProfile')
        calculation_method = request.form.get('calculationMethod')
        social_security_claim_age = int(request.form.get('socialSecurityClaimAge'))
        
        # Spouse data
        spouse_birth_year = request.form.get('spouseBirthYear')
        
        both_working = request.form.get('bothWorking')
        spouse_annual_income = request.form.get('spouseAnnualIncome')
        spouse_years_worked = request.form.get('spouseYearsWorked')
        spouse_annual_contribution = request.form.get('spouseAnnualContribution')
        spouse_social_security_claim_age = request.form.get('spouseSocialSecurityClaimAge')
        
        # Budget data
        housing = float(request.form.get('housing'))
        
        # Get healthcare estimate if not provided
        healthcare_input = request.form.get('healthcare')
        if healthcare_input and float(healthcare_input) > 0:
            healthcare = float(healthcare_input)
        else:
            # Auto-estimate healthcare based on age, income, and location
            state = request.form.get('state')
            zip_code = request.form.get('zipCode')
            tobacco_use = request.form.get('tobaccoUse') == 'true'
            
            if state and zip_code:
                # Estimate healthcare for primary person at retirement age
                primary_healthcare = estimate_healthcare_premiums(
                    age=retirement_age,
                    income=annual_income,
                    state=state,
                    zip_code=zip_code,
                    tobacco_use=tobacco_use
                )
                
                # Estimate healthcare for spouse at their retirement age if applicable
                spouse_healthcare = 0
                if marital_status != 'single' and spouse_birth_year:
                    # Calculate spouse's age at primary person's retirement
                    spouse_age_at_retirement = retirement_age - (birth_year - int(spouse_birth_year))
                    spouse_income = spouse_annual_income if both_working == 'both' else annual_income
                    
                    spouse_healthcare_estimate = estimate_healthcare_premiums(
                        age=spouse_age_at_retirement,
                        income=spouse_income,
                        state=state,
                        zip_code=zip_code,
                        tobacco_use=tobacco_use
                    )
                    spouse_healthcare = spouse_healthcare_estimate['estimated_annual_cost']
                
                healthcare = primary_healthcare['estimated_annual_cost'] + spouse_healthcare
            else:
                # Default fallback - estimate for both if couple
                if marital_status != 'single':
                    healthcare = 24000  # $12,000 per person for couple
                else:
                    healthcare = 12000  # $12,000 for single person
        
        food_living = float(request.form.get('foodLiving'))
        travel_leisure = float(request.form.get('travelLeisure'))
        other_discretionary = float(request.form.get('otherDiscretionary'))
        
        # Calculate current age and years to retirement
        current_year = datetime.now().year
        current_age = current_year - birth_year
        years_to_retirement = retirement_age - current_age
        
        # Calculate portfolio growth during working years
        portfolio_balance = liquid_assets
        if calculation_method == 'monteCarlo':
            portfolio_balance = monte_carlo_simulation(
                portfolio_balance, annual_contribution, years_to_retirement, market_profile
            )
        else:
            portfolio_balance = deterministic_growth(
                portfolio_balance, annual_contribution, years_to_retirement, market_profile
            )
        
        # Calculate Social Security benefits
        primary_social_security = 0
        spousal_social_security = 0
        
        # Calculate Social Security benefits - they start at claim age regardless of retirement age
        primary_social_security = calculate_social_security_benefit(
            birth_year, annual_income, years_worked, social_security_claim_age
        )
        
        if marital_status != 'single':
            if both_working == 'both' and spouse_annual_income and spouse_years_worked:
                # Both working - calculate separately
                if spouse_social_security_claim_age:
                    spousal_social_security = calculate_social_security_benefit(
                        int(spouse_birth_year), float(spouse_annual_income), 
                        int(spouse_years_worked), int(spouse_social_security_claim_age)
                    )
            else:
                # Only one working - calculate spousal benefit
                spousal_social_security = calculate_spousal_benefit(
                    primary_social_security, int(spouse_birth_year), birth_year
                )
        
        # Calculate total annual income
        real_estate_income = real_estate_cashflow
        total_social_security = primary_social_security + spousal_social_security
        safe_withdrawal = calculate_safe_withdrawal(portfolio_balance)
        total_annual_income = safe_withdrawal + real_estate_income + total_social_security
        
        # Calculate annual budget
        annual_budget = housing + healthcare + food_living + travel_leisure + other_discretionary
        surplus_deficit = total_annual_income - annual_budget
        
        # Generate comprehensive forecast including working years and retirement
        forecast = []
        current_portfolio = liquid_assets  # Start with current assets
        
        # First, show working years (from current age to retirement)
        for year in range(years_to_retirement + 1):
            current_year_age = current_age + year
            starting_balance = current_portfolio
            
            # Calculate investment gains during working years
            if market_profile == 'Conservative':
                mean_return = 0.05
            elif market_profile == 'Moderate':
                mean_return = 0.07
            else:  # Aggressive
                mean_return = 0.09
            
            investment_gains = starting_balance * mean_return
            
            # During working years: no real estate income, no Social Security, no retirement spending
            real_estate_cashflow_year = 0
            social_security_year = 0
            spending = 0
            
            # Add annual contribution during working years
            contribution = annual_contribution if year < years_to_retirement else 0
            
            # Ending balance
            ending_balance = starting_balance + investment_gains + contribution
            current_portfolio = ending_balance
            
            forecast.append({
                'age': current_year_age,
                'year': current_year + year,
                'startingBalance': round(starting_balance),
                'investmentGains': round(investment_gains),
                'realEstateCashflow': round(real_estate_cashflow_year),
                'socialSecurity': round(social_security_year),
                'spending': round(spending),
                'endingBalance': round(ending_balance),
                'contribution': round(contribution),
                'period': 'Working'
            })
        
        # Then show retirement years (30 years of retirement)
        for year in range(30):
            age = retirement_age + year
            starting_balance = current_portfolio
            
            # Calculate investment gains during retirement
            if market_profile == 'Conservative':
                mean_return = 0.05
            elif market_profile == 'Moderate':
                mean_return = 0.07
            else:  # Aggressive
                mean_return = 0.09
            
            investment_gains = starting_balance * mean_return
            
            # Real estate income starts in retirement
            real_estate_cashflow_year = real_estate_income
            
            # Social Security starts at specified claim age
            social_security_year = 0
            if age >= social_security_claim_age:
                social_security_year += primary_social_security
            if marital_status != 'single' and spouse_social_security_claim_age and age >= int(spouse_social_security_claim_age):
                social_security_year += spousal_social_security
            
            # Retirement spending starts
            spending = annual_budget
            
            # Ending balance
            ending_balance = starting_balance + investment_gains + real_estate_cashflow_year + social_security_year - spending
            current_portfolio = ending_balance
            
            forecast.append({
                'age': age,
                'year': current_year + years_to_retirement + year,
                'startingBalance': round(starting_balance),
                'investmentGains': round(investment_gains),
                'realEstateCashflow': round(real_estate_cashflow_year),
                'socialSecurity': round(social_security_year),
                'spending': round(spending),
                'endingBalance': round(ending_balance),
                'contribution': 0,
                'period': 'Retirement'
            })
        
        # Calculate safe sustainable spending
        safe_sustainable_spending = calculate_sustainable_spending(
            portfolio_balance, real_estate_income, total_social_security, annual_budget
        )
        
        # Generate chart data for portfolio balance over time
        portfolio_balance_chart = []
        for year_data in forecast:
            portfolio_balance_chart.append({
                'year': year_data['year'],
                'age': year_data['age'],
                'balance': year_data['endingBalance'],
                'period': year_data['period']
            })
        
        # Generate extended asset growth chart to age 100
        extended_asset_chart = []
        current_age = current_year - birth_year
        current_portfolio_value = liquid_assets
        
        # Project from current year to age 100
        for age in range(current_age, 101):
            year = current_year + (age - current_age)
            
            if age < retirement_age:
                # Working years: contributions + investment growth
                if age == current_age:
                    starting_balance = current_portfolio_value
                else:
                    starting_balance = extended_asset_chart[-1]['totalAssets']
                
                # Investment growth based on risk tolerance
                if market_profile == 'Conservative':
                    mean_return = 0.06
                elif market_profile == 'Moderate':
                    mean_return = 0.075
                else:  # Aggressive
                    mean_return = 0.09
                
                investment_gains = starting_balance * mean_return
                contribution = annual_contribution
                real_estate_income = 0
                social_security = 0
                spending = 0
                
                ending_balance = starting_balance + investment_gains + contribution + real_estate_income + social_security - spending
                total_assets = ending_balance
                
            else:
                # Retirement years: withdrawals + investment growth
                if age == retirement_age:
                    starting_balance = portfolio_balance
                else:
                    starting_balance = extended_asset_chart[-1]['totalAssets']
                
                # Investment growth based on risk tolerance
                if market_profile == 'Conservative':
                    mean_return = 0.05  # Slightly more conservative in retirement
                elif market_profile == 'Moderate':
                    mean_return = 0.065
                else:  # Aggressive
                    mean_return = 0.08
                
                investment_gains = starting_balance * mean_return
                contribution = 0
                
                # Real estate income
                real_estate_income = real_estate_cashflow
                
                # Social Security
                social_security = 0
                if age >= social_security_claim_age:
                    social_security += primary_social_security
                if marital_status != 'single' and spouse_social_security_claim_age and age >= int(spouse_social_security_claim_age):
                    social_security += spousal_social_security
                
                # Retirement spending
                spending = annual_budget
                
                ending_balance = starting_balance + investment_gains + contribution + real_estate_income + social_security - spending
                total_assets = ending_balance
            
            extended_asset_chart.append({
                'year': year,
                'age': age,
                'totalAssets': round(total_assets),
                'period': 'Working' if age < retirement_age else 'Retirement',
                'contributions': contribution,
                'investmentGains': round(investment_gains),
                'realEstateIncome': round(real_estate_income),
                'socialSecurity': round(social_security),
                'spending': round(spending)
            })
        
        # Add Social Security calculation details for validation
        social_security_details = {
            'primaryFRA': calculate_social_security_benefit(birth_year, annual_income, years_worked, 67),
            'primaryClaimed': primary_social_security,
            'spousalFRA': calculate_spousal_benefit(
                calculate_social_security_benefit(birth_year, annual_income, years_worked, 67), 
                int(spouse_birth_year) if spouse_birth_year else 0, 
                birth_year
            ) if marital_status != 'single' else 0,
            'spousalClaimed': spousal_social_security,
            'totalFRA': calculate_social_security_benefit(birth_year, annual_income, years_worked, 67) + 
                       (calculate_spousal_benefit(
                           calculate_social_security_benefit(birth_year, annual_income, years_worked, 67), 
                           int(spouse_birth_year) if spouse_birth_year else 0, 
                           birth_year
                       ) if marital_status != 'single' else 0),
            'totalClaimed': total_social_security
        }
        
        results = {
            'forecast': forecast,
            'summary': {
                'portfolioAtRetirement': round(portfolio_balance),
                'safeAnnualWithdrawal': round(safe_withdrawal),
                'totalAnnualIncome': round(total_annual_income),
                'annualBudget': round(annual_budget),
                'surplusDeficit': round(surplus_deficit),
                'safeSustainableSpending': round(safe_sustainable_spending)
            },
            'budget': {
                'housing': housing,
                'healthcare': healthcare,
                'foodLiving': food_living,
                'travelLeisure': travel_leisure,
                'otherDiscretionary': other_discretionary
            },
            'socialSecurityDetails': social_security_details,
            'realEstateCashflow': round(real_estate_income),
            'portfolioBalanceChart': portfolio_balance_chart,
            'extendedAssetChart': extended_asset_chart,
            'yearsToRetirement': years_to_retirement
        }
        
        return render_template_string(HTML_TEMPLATE, results=results)
        
    except Exception as e:
        return f"Error: {str(e)}", 400

def calculate_social_security_benefit(birth_year, annual_income, years_worked, claim_age):
    """Calculate Social Security benefit based on birth year, income, years worked, and claim age."""
    fra = 67  # Full Retirement Age for birth year >= 1960
    
    # 2024 Social Security Maximum Benefit at FRA (age 67): $45,864/year
    MAX_FRA_BENEFIT = 45864
    
    # Calculate FRA benefit (Primary Insurance Amount) - approximately 40% of average annual income
    fra_benefit = annual_income * 0.4
    
    # Adjust for years worked (assuming 35 years is full career)
    years_adjustment = min(years_worked / 35, 1)
    fra_benefit *= years_adjustment
    
    # Apply maximum benefit cap
    fra_benefit = min(fra_benefit, MAX_FRA_BENEFIT)
    
    # Adjust for early/late claiming
    if claim_age == 62:
        benefit = fra_benefit * 0.7  # 70% of FRA benefit (as per worked example)
    elif claim_age == 70:
        benefit = fra_benefit * 1.32  # 132% of FRA benefit
    else:
        # Linear interpolation for ages between 62 and 70
        age_diff = claim_age - 62
        benefit_increase = (0.32 * age_diff) / 8
        benefit = fra_benefit * (0.7 + benefit_increase)
    
    return round(benefit)

def calculate_spousal_benefit(working_spouse_benefit, non_working_spouse_birth_year, working_spouse_birth_year):
    """Calculate spousal benefit for non-working spouse."""
    fra = 67
    current_year = datetime.now().year
    non_working_spouse_age = current_year - non_working_spouse_birth_year
    
    # Spousal benefit is up to 50% of working spouse's FRA benefit
    spousal_benefit = working_spouse_benefit * 0.5
    
    # Adjust for early claiming (spousal benefit doesn't increase with delayed retirement)
    # Based on worked example: if claimed at 62, reduced to ~35% of worker's FRA benefit
    if non_working_spouse_age < fra:
        # More accurate reduction: from 50% to 35% when claiming at 62
        # This gives us a reduction factor of 0.3 (50% - 35% = 15% reduction)
        # For each year before FRA, reduce by approximately 3% (15% / 5 years = 3% per year)
        reduction = (fra - non_working_spouse_age) * 0.03
        spousal_benefit *= (1 - reduction)
    
    return round(spousal_benefit)

def monte_carlo_simulation(initial_balance, annual_contribution, years, market_profile):
    """Monte Carlo simulation for portfolio growth."""
    if market_profile == 'Conservative':
        mean, std_dev = 0.05, 0.12
    elif market_profile == 'Moderate':
        mean, std_dev = 0.07, 0.15
    else:  # Aggressive
        mean, std_dev = 0.09, 0.18
    
    current_balance = initial_balance
    
    for year in range(years):
        # Generate random return for this year
        random_return = mean + (random.random() - 0.5) * 2 * std_dev
        current_balance = current_balance * (1 + random_return) + annual_contribution
    
    return current_balance

def deterministic_growth(initial_balance, annual_contribution, years, market_profile):
    """Deterministic growth calculation."""
    if market_profile == 'Conservative':
        mean = 0.05
    elif market_profile == 'Moderate':
        mean = 0.07
    else:  # Aggressive
        mean = 0.09
    
    current_balance = initial_balance
    
    for year in range(years):
        current_balance = current_balance * (1 + mean) + annual_contribution
    
    return current_balance

def calculate_safe_withdrawal(portfolio_balance):
    """Calculate safe withdrawal rate (4% rule)."""
    return portfolio_balance * 0.04

def estimate_healthcare_premiums(age, income, state, zip_code, tobacco_use=False, year=2024):
    """
    Estimate healthcare premiums using CMS Marketplace API data.
    Returns estimated monthly and annual premiums for different metal tiers.
    
    Based on CMS Marketplace API documentation:
    - Endpoint: https://marketplace.cms.gov/api/v1/plans/search
    - Documentation: https://marketplace.cms.gov/developers
    - GitHub: https://github.com/Quantum-One-DLT/aca-marketplace-api-js
    """
    try:
        # CMS Marketplace API endpoint for plan search
        api_url = "https://marketplace.cms.gov/api/v1/plans/search"
        
        # Prepare the API request payload according to CMS documentation
        payload = {
            "year": year,
            "state": state,
            "zip_code": zip_code,
            "household_size": 1,  # Single person for now
            "household_income": income,
            "age": age,
            "tobacco_use": tobacco_use,
            "metal_level": ["Bronze", "Silver", "Gold", "Platinum"],
            "plan_type": ["HMO", "PPO", "EPO", "POS"],
            "limit": 50
        }
        
        # Make the API request to CMS Marketplace
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Retirement-Planning-App/1.0'
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Parse the CMS API response
                api_data = response.json()
                
                # Extract premium information from the API response
                premiums = {}
                out_of_pocket_info = {}
                
                for plan in api_data.get('plans', []):
                    metal_level = plan.get('metal_level')
                    if metal_level not in premiums:
                        premiums[metal_level] = {
                            'monthly': plan.get('premium', 0),
                            'annual': plan.get('premium', 0) * 12
                        }
                        out_of_pocket_info[metal_level] = {
                            'deductible': plan.get('deductible', 0),
                            'max_out_of_pocket': plan.get('max_out_of_pocket', 0)
                        }
                
                # If API returns data, use it
                if premiums:
                    # Calculate subsidies based on income and federal poverty level
                    fpl_single = 14580  # 2024 Federal Poverty Level for single person
                    subsidy_eligible = income <= fpl_single * 4  # 400% of FPL
                    
                    if subsidy_eligible:
                        # Apply ACA subsidies to Silver plan
                        subsidy_percentage = max(0, (fpl_single * 4 - income) / (fpl_single * 4))
                        if 'Silver' in premiums:
                            premiums['Silver']['monthly'] *= (1 - subsidy_percentage * 0.8)
                            premiums['Silver']['annual'] = premiums['Silver']['monthly'] * 12
                    else:
                        subsidy_percentage = 0
                    
                    # Determine recommended plan and estimated annual cost
                    recommended_tier = 'Silver' if subsidy_eligible else 'Bronze'
                    estimated_annual_cost = premiums[recommended_tier]['annual'] + out_of_pocket_info[recommended_tier]['deductible']
                    
                    return {
                        'premiums': premiums,
                        'out_of_pocket': out_of_pocket_info,
                        'subsidy_eligible': subsidy_eligible,
                        'subsidy_percentage': round(subsidy_percentage * 100, 1) if subsidy_eligible else 0,
                        'estimated_annual_cost': estimated_annual_cost,
                        'recommended_tier': recommended_tier,
                        'source': 'CMS Marketplace API'
                    }
        
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            # Fall through to fallback calculation
        
        # Fallback calculation using realistic estimates based on CMS data patterns
        # This provides estimates when the API is unavailable or returns no data
        
        # Base premium estimates by age and income (based on CMS marketplace data)
        base_premiums = {
            'Bronze': {
                'monthly': 350 + (age - 50) * 15,  # Base + age adjustment
                'annual': 0
            },
            'Silver': {
                'monthly': 450 + (age - 50) * 20,
                'annual': 0
            },
            'Gold': {
                'monthly': 550 + (age - 50) * 25,
                'annual': 0
            },
            'Platinum': {
                'monthly': 700 + (age - 50) * 30,
                'annual': 0
            }
        }
        
        # Calculate annual premiums
        for tier in base_premiums:
            base_premiums[tier]['annual'] = base_premiums[tier]['monthly'] * 12
        
        # Income-based adjustments (ACA subsidies)
        fpl_single = 14580
        subsidy_eligible = income <= fpl_single * 4
        
        if subsidy_eligible:
            subsidy_threshold = fpl_single * 4
            subsidy_percentage = max(0, (subsidy_threshold - income) / subsidy_threshold)
            # Apply subsidies to Silver plan (most common for subsidies)
            base_premiums['Silver']['monthly'] *= (1 - subsidy_percentage * 0.8)  # Max 80% subsidy
            base_premiums['Silver']['annual'] = base_premiums['Silver']['monthly'] * 12
        else:
            subsidy_percentage = 0
        
        # Tobacco use adjustment (typically 50% increase)
        if tobacco_use:
            for tier in base_premiums:
                base_premiums[tier]['monthly'] *= 1.5
                base_premiums[tier]['annual'] *= 1.5
        
        # State-specific adjustments (based on CMS data patterns)
        state_adjustments = {
            'CA': 1.1, 'NY': 1.15, 'TX': 0.9, 'FL': 0.95, 'IL': 1.05,
            'PA': 1.0, 'OH': 0.9, 'GA': 0.85, 'NC': 0.9, 'MI': 0.95
        }
        
        if state in state_adjustments:
            for tier in base_premiums:
                base_premiums[tier]['monthly'] *= state_adjustments[state]
                base_premiums[tier]['annual'] *= state_adjustments[state]
        
        # Add out-of-pocket maximums and deductibles (typical CMS values)
        out_of_pocket_info = {
            'Bronze': {'deductible': 7000, 'max_out_of_pocket': 9100},
            'Silver': {'deductible': 5000, 'max_out_of_pocket': 9100},
            'Gold': {'deductible': 2000, 'max_out_of_pocket': 9100},
            'Platinum': {'deductible': 0, 'max_out_of_pocket': 9100}
        }
        
        # Determine recommended plan and estimated annual cost
        recommended_tier = 'Silver' if subsidy_eligible else 'Bronze'
        estimated_annual_cost = base_premiums[recommended_tier]['annual'] + out_of_pocket_info[recommended_tier]['deductible']
        
        return {
            'premiums': base_premiums,
            'out_of_pocket': out_of_pocket_info,
            'subsidy_eligible': subsidy_eligible,
            'subsidy_percentage': round(subsidy_percentage * 100, 1) if subsidy_eligible else 0,
            'estimated_annual_cost': estimated_annual_cost,
            'recommended_tier': recommended_tier,
            'source': 'Fallback Calculation (CMS data patterns)'
        }
        
    except Exception as e:
        print(f"Healthcare estimation error: {e}")
        # Ultimate fallback to basic estimates
        fallback_estimate = {
            'premiums': {
                'Bronze': {'monthly': 400, 'annual': 4800},
                'Silver': {'monthly': 500, 'annual': 6000},
                'Gold': {'monthly': 600, 'annual': 7200},
                'Platinum': {'monthly': 800, 'annual': 9600}
            },
            'out_of_pocket': {
                'Bronze': {'deductible': 7000, 'max_out_of_pocket': 9100},
                'Silver': {'deductible': 5000, 'max_out_of_pocket': 9100},
                'Gold': {'deductible': 2000, 'max_out_of_pocket': 9100},
                'Platinum': {'deductible': 0, 'max_out_of_pocket': 9100}
            },
            'subsidy_eligible': False,
            'subsidy_percentage': 0,
            'estimated_annual_cost': 11000,
            'recommended_tier': 'Silver',
            'source': 'Basic Fallback'
        }
        return fallback_estimate

def calculate_sustainable_spending(portfolio_balance, real_estate_income, social_security_income, expenses):
    """Calculate sustainable spending based on portfolio and other income sources."""
    safe_withdrawal = calculate_safe_withdrawal(portfolio_balance)
    total_income = safe_withdrawal + real_estate_income + social_security_income
    
    # Return the sustainable spending amount (not limited by budget)
    # This represents the maximum amount you can safely spend annually
    return total_income

if __name__ == '__main__':
    print("Starting Retirement Planning Calculator...")
    print("Open your browser and go to: http://localhost:5001")
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
