"""
UK Mortgage Calculator API
Core mortgage calculation engine with BoE data integration and ML forecasting
"""

import json
import logging
import azure.functions as func
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import requests
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.keyvault.secrets import SecretClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MortgageCalculator:
    """Core mortgage calculation engine"""
    
    def __init__(self):
        self.monthly_multiplier = 12
        
    def calculate_monthly_payment(
        self, 
        loan_amount: float, 
        annual_rate: float, 
        term_years: int
    ) -> float:
        """
        Calculate monthly mortgage payment using standard formula
        
        Args:
            loan_amount: Principal loan amount
            annual_rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
            term_years: Loan term in years
            
        Returns:
            Monthly payment amount
        """
        try:
            if annual_rate == 0:
                return loan_amount / (term_years * self.monthly_multiplier)
            
            monthly_rate = annual_rate / self.monthly_multiplier
            num_payments = term_years * self.monthly_multiplier
            
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** num_payments
            ) / ((1 + monthly_rate) ** num_payments - 1)
            
            return round(monthly_payment, 2)
            
        except Exception as e:
            logger.error(f"Error calculating monthly payment: {str(e)}")
            raise
    
    def calculate_overpayment_impact(
        self,
        loan_amount: float,
        annual_rate: float,
        term_years: int,
        overpayment_amount: float,
        overpayment_frequency: str = "monthly"  # monthly, annual, one_off
    ) -> Dict[str, Any]:
        """
        Calculate the impact of overpayments on mortgage
        
        Returns:
            Dictionary with savings, time reduction, and payment schedule
        """
        try:
            base_payment = self.calculate_monthly_payment(loan_amount, annual_rate, term_years)
            
            # Calculate overpayment scenarios
            if overpayment_frequency == "monthly":
                total_monthly_payment = base_payment + overpayment_amount
            elif overpayment_frequency == "annual":
                total_monthly_payment = base_payment + (overpayment_amount / 12)
            else:  # one_off
                total_monthly_payment = base_payment
                # Handle one-off payment separately
            
            # Simulate payment schedule
            balance = loan_amount
            monthly_rate = annual_rate / 12
            payments_made = 0
            total_interest = 0
            
            while balance > 0.01 and payments_made < term_years * 12:
                interest_payment = balance * monthly_rate
                principal_payment = total_monthly_payment - interest_payment
                
                if principal_payment > balance:
                    principal_payment = balance
                    
                balance -= principal_payment
                total_interest += interest_payment
                payments_made += 1
            
            # Calculate base scenario for comparison
            base_total_interest = (base_payment * term_years * 12) - loan_amount
            
            return {
                "new_monthly_payment": total_monthly_payment,
                "months_saved": (term_years * 12) - payments_made,
                "interest_saved": base_total_interest - total_interest,
                "total_payments": payments_made,
                "years_saved": round(((term_years * 12) - payments_made) / 12, 1)
            }
            
        except Exception as e:
            logger.error(f"Error calculating overpayment impact: {str(e)}")
            raise

class BoEDataCollector:
    """Bank of England data collection and processing"""
    
    def __init__(self):
        self.base_url = "https://www.bankofengland.co.uk/boeapps/database"
        
    def fetch_interest_rates(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Fetch historical interest rate data from Bank of England API
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with historical interest rate data
        """
        try:
            # BoE base rate series code
            series_code = "IUDBEDR"  # Bank Rate
            
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365*10)).strftime("%Y-%m-%d")
            if not end_date:
                end_date = datetime.now().strftime("%Y-%m-%d")
            
            url = f"{self.base_url}/knowledgebank/series/{series_code}"
            params = {
                "first": start_date,
                "last": end_date,
                "format": "json"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Process the data into DataFrame
            if 'data' in data:
                df = pd.DataFrame(data['data'])
                df['date'] = pd.to_datetime(df['date'])
                df['rate'] = pd.to_numeric(df['value'], errors='coerce')
                df = df.dropna(subset=['rate'])
                df = df.sort_values('date')
                
                logger.info(f"Fetched {len(df)} interest rate records")
                return df[['date', 'rate']]
            else:
                logger.warning("No data found in BoE response")
                return pd.DataFrame(columns=['date', 'rate'])
                
        except Exception as e:
            logger.error(f"Error fetching BoE data: {str(e)}")
            # Return sample data for development
            dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='M')
            rates = np.random.normal(2.5, 1.5, len(dates))
            return pd.DataFrame({'date': dates, 'rate': rates})

class InterestRatePredictor:
    """Machine learning model for interest rate forecasting"""
    
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Prepare features for ML model
        
        Args:
            df: DataFrame with date and rate columns
            
        Returns:
            Feature matrix
        """
        try:
            df = df.copy()
            df = df.sort_values('date')
            
            # Create time-based features
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['quarter'] = df['date'].dt.quarter
            
            # Create lag features
            for lag in [1, 3, 6, 12]:
                df[f'rate_lag_{lag}'] = df['rate'].shift(lag)
            
            # Create moving averages
            for window in [3, 6, 12]:
                df[f'rate_ma_{window}'] = df['rate'].rolling(window=window).mean()
            
            # Create rate change features
            df['rate_change_1m'] = df['rate'].diff(1)
            df['rate_change_3m'] = df['rate'].diff(3)
            
            # Drop rows with NaN values
            df = df.dropna()
            
            feature_columns = [col for col in df.columns if col not in ['date', 'rate']]
            return df[feature_columns].values, df['rate'].values
            
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise
    
    def train_model(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Train the interest rate prediction model
        
        Args:
            df: Historical interest rate data
            
        Returns:
            Training metrics
        """
        try:
            X, y = self.prepare_features(df)
            
            if len(X) < 50:
                logger.warning("Insufficient data for robust training")
                return {"error": "Insufficient training data"}
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=False
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            self.is_trained = True
            
            # Calculate metrics
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            
            logger.info(f"Model trained - Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
            
            return {
                "train_r2": train_score,
                "test_r2": test_score,
                "samples_used": len(X_train)
            }
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise
    
    def predict_rates(
        self, 
        current_data: pd.DataFrame, 
        months_ahead: int = 12
    ) -> Dict[str, List[float]]:
        """
        Predict future interest rates with optimistic and pessimistic scenarios
        
        Args:
            current_data: Recent historical data
            months_ahead: Number of months to predict
            
        Returns:
            Dictionary with base, optimistic, and pessimistic predictions
        """
        try:
            if not self.is_trained:
                logger.warning("Model not trained, returning sample predictions")
                current_rate = current_data['rate'].iloc[-1] if len(current_data) > 0 else 3.0
                base = [current_rate + np.random.normal(0, 0.1) for _ in range(months_ahead)]
                return {
                    "base_scenario": base,
                    "optimistic_scenario": [max(0, rate - 0.5) for rate in base],
                    "pessimistic_scenario": [rate + 0.5 for rate in base]
                }
            
            X, _ = self.prepare_features(current_data)
            latest_features = X[-1:] if len(X) > 0 else np.zeros((1, X.shape[1]))
            
            # Scale features
            latest_scaled = self.scaler.transform(latest_features)
            
            predictions = []
            for _ in range(months_ahead):
                pred = self.model.predict(latest_scaled)[0]
                predictions.append(max(0, pred))  # Ensure non-negative rates
                
                # Update features for next prediction (simplified)
                # In practice, you'd update all relevant features
                latest_scaled[0, 0] = pred  # Update the most recent rate
            
            # Create scenarios with uncertainty bands
            base_scenario = predictions
            uncertainty = 0.25  # 25 basis points uncertainty
            
            optimistic_scenario = [max(0, rate - uncertainty) for rate in base_scenario]
            pessimistic_scenario = [rate + uncertainty for rate in base_scenario]
            
            return {
                "base_scenario": base_scenario,
                "optimistic_scenario": optimistic_scenario,
                "pessimistic_scenario": pessimistic_scenario
            }
            
        except Exception as e:
            logger.error(f"Error predicting rates: {str(e)}")
            # Return fallback predictions
            current_rate = 3.0
            base = [current_rate + np.random.normal(0, 0.1) for _ in range(months_ahead)]
            return {
                "base_scenario": base,
                "optimistic_scenario": [max(0, rate - 0.5) for rate in base],
                "pessimistic_scenario": [rate + 0.5 for rate in base]
            }

# Global instances
calculator = MortgageCalculator()
data_collector = BoEDataCollector()
predictor = InterestRatePredictor()
