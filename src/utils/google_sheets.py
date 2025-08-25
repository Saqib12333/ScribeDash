"""
Google Sheets integration module for ScribeDash
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import time
import hashlib
import gspread
import logging
from google.oauth2.service_account import Credentials
import json
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


class GoogleSheetsConnector:
    """Google Sheets connector with caching and rate limiting"""
    
    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes cache
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests
        self.client = None
        self.spreadsheet = None
        self._initialize_connection()
        
    def _initialize_connection(self):
        """Initialize Google Sheets connection"""
        try:
            credentials_path = Path(__file__).parent.parent.parent / "config" / "credentials.json"
            if credentials_path.exists():
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive",
                ]
                creds = Credentials.from_service_account_file(str(credentials_path), scopes=scope)
                self.client = gspread.authorize(creds)
                self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
                logger.info("Connected to Google Sheets successfully")
                st.session_state['sheets_connected'] = True
            else:
                logger.warning("Credentials file not found. Falling back to sample data")
                st.session_state['sheets_connected'] = False
        except Exception as e:
            logger.warning(f"Could not connect to Google Sheets: {str(e)}. Using sample data")
            st.session_state['sheets_connected'] = False
            self.client = None
        
    def _rate_limit(self):
        """Implement rate limiting to avoid API quota issues"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        self.last_request_time = time.time()
    
    def _get_cache_key(self, sheet_name: str, range_name: Optional[str] = None) -> str:
        """Generate cache key for requests"""
        key_data = f"{sheet_name}_{range_name}_{self.spreadsheet_id}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key]['timestamp']
        return (time.time() - cached_time) < self.cache_ttl
    
    def get_sheet_data(self, sheet_name: str, use_cache: bool = True) -> pd.DataFrame:
        """
        Get data from a specific sheet
        
        Args:
            sheet_name: Name of the sheet tab
            use_cache: Whether to use cached data
            
        Returns:
            DataFrame with sheet data
        """
        cache_key = self._get_cache_key(sheet_name)
        
        # Return cached data if valid
        if use_cache and self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data'].copy()
        
        try:
            # Try to get real data if connected
            if self.client and self.spreadsheet:
                self._rate_limit()
                
                # Get the worksheet
                worksheet = self.spreadsheet.worksheet(sheet_name)
                
                # Get all values
                data_values = worksheet.get_all_values()
                
                if data_values:
                    # Convert to DataFrame
                    headers = data_values[0]
                    rows = data_values[1:]
                    data = pd.DataFrame(rows, columns=headers)
                    
                    # Clean up the data
                    data = self._clean_dataframe(data)
                else:
                    data = pd.DataFrame()
            else:
                # Fallback to sample data
                data = self._generate_sample_data(sheet_name)
            
            # Cache the data
            if use_cache:
                self.cache[cache_key] = {
                    'data': data.copy(),
                    'timestamp': time.time()
                }
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data from sheet '{sheet_name}': {str(e)}")
            return pd.DataFrame()
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and process dataframe from Google Sheets"""
        try:
            logger.info(f"Cleaning dataframe with shape: {df.shape}")
            if df.empty:
                logger.info("DataFrame is empty, returning as-is")
                return df
            
            # Remove completely empty rows and columns
            initial_shape = df.shape
            df = df.dropna(how='all')
            logger.info(f"After removing empty rows: {initial_shape} -> {df.shape}")
            
            # Remove unnamed columns safely
            if hasattr(df.columns, 'str'):
                unnamed_mask = df.columns.str.contains('^Unnamed', na=False)
                df = df.loc[:, ~unnamed_mask]
                logger.info(f"After removing unnamed columns: {df.shape}")
            
            # Try to convert numeric columns
            for col in df.columns:
                try:
                    # Skip empty column names
                    if not col or str(col).strip() == '':
                        logger.debug("Skipping empty column name")
                        continue
                        
                    # Skip if all values are empty/null - use proper boolean checking
                    if len(df[col]) == 0:
                        logger.debug(f"Column '{col}' is empty, skipping")
                        continue
                    
                    # Check if all values are null/empty using sum() instead of all()
                    is_all_null = df[col].isna().sum() == len(df[col])
                    if is_all_null:
                        logger.debug(f"Column '{col}' is all null, skipping")
                        continue
                        
                    # Try to convert to numeric (handles percentages, currencies, etc.)
                    # Convert to string first
                    str_col = df[col].astype(str)
                    # Clean common non-numeric characters
                    cleaned_col = str_col.str.replace(r'[%$,]', '', regex=True)
                    # Replace 'nan' and empty strings with actual NaN
                    cleaned_col = cleaned_col.replace(['nan', '', 'None'], pd.NA)
                    # Convert to numeric
                    numeric_col = pd.to_numeric(cleaned_col, errors='coerce')
                    
                    # Only replace if we got some numeric values - avoid Series ambiguity
                    null_count = numeric_col.isna().sum()
                    total_count = len(numeric_col)
                    if null_count < total_count:  # Some values were successfully converted
                        df[col] = numeric_col
                        logger.debug(f"Converted column '{col}' to numeric")
                    else:
                        logger.debug(f"Column '{col}' could not be converted to numeric")
                        
                except Exception as col_error:
                    # Keep original values if conversion fails for this column
                    logger.warning(f"Could not process column '{col}': {str(col_error)}")
                    continue
            
            logger.info(f"Data cleaning completed successfully. Final shape: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Error in _clean_dataframe: {str(e)}", exc_info=True)
            return df  # Return original dataframe if cleaning fails
    
    def get_all_sheets(self) -> Dict[str, pd.DataFrame]:
        """Get data from all sheets"""
        sheets = [
            'Dataset',
            'Patient Count', 
            'Utilization',
            'August'  # Current month
        ]
        
        logger.info(f"Loading {len(sheets)} sheets: {sheets}")
        all_data = {}
        for sheet_name in sheets:
            try:
                logger.info(f"Loading sheet: {sheet_name}")
                all_data[sheet_name] = self.get_sheet_data(sheet_name)
                logger.info(f"Successfully loaded sheet '{sheet_name}' with {len(all_data[sheet_name])} rows")
            except Exception as e:
                logger.error(f"Could not load sheet '{sheet_name}': {str(e)}")
                st.warning(f"Could not load sheet '{sheet_name}': {str(e)}")
                all_data[sheet_name] = pd.DataFrame()
        
        logger.info(f"Completed loading all sheets. Total: {len(all_data)}")
        return all_data
    
    def _generate_sample_data(self, sheet_name: str) -> pd.DataFrame:
        """Generate sample data for demonstration purposes"""
        
        if sheet_name == 'Dataset':
            return self._generate_main_dataset()
        elif sheet_name == 'Patient Count':
            return self._generate_patient_count_data()
        elif sheet_name == 'Utilization':
            return self._generate_utilization_data()
        elif sheet_name in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']:
            return self._generate_monthly_data(sheet_name)
        else:
            return pd.DataFrame()
    
    def _generate_main_dataset(self) -> pd.DataFrame:
        """Generate sample main dataset"""
        # Real scribes data from the team
        haider_team = [
            "Shivam Chauhan", "Sutirtha Chakraborty", "Ansika Negi", "Prachi Sharma", 
            "Prarthana Sinha Roy", "Akshita Pandey", "Rohan Setia", "Nikhil Yadav", 
            "Vaibhavi Mittal", "Ayushi Singh", "Deepa Deepak", "Tenzin Wangmo", 
            "Piyush Sharma", "Debraj Dey", "Priyanka Bhadauria", "Solomon Raju", 
            "Rozy Chugh", "Ashutosh Srivastava"
        ]
        
        saqib_team = [
            "Manvitha Gullipalli", "Samir Bhattacharya", "Pankaj Kumar Singh", "Amisha Raj", 
            "Navya Dwivedi", "Puja Agarwal", "Dhriti Shukla", "Bijaya Biswas", 
            "Devansh Sharma", "Pragya Pal", "Vaydoorya", "Deepak Devasia", 
            "Iqra Khan", "Bithika Maji", "Bagmita Borah", "Ayushi Aggarwal", 
            "Amandeep Chauhan", "Sakshi Sharma", "Suruchi Bhatia", "Sarthak Kapoor"
        ]
        
        all_scribes = []
        
        # Generate data for Haider Khan team
        for scribe in haider_team:
            all_scribes.append({
                'Scribe Name': scribe,
                'Team Leader': 'Haider Khan',
                'Monthly Patients': np.random.randint(60, 120),
                'Efficiency Score': np.random.uniform(85, 98),
                'Avg Session Length': np.random.uniform(2.5, 4.5),
                'Provider Rating': np.random.uniform(4.0, 5.0),
                'Attendance Rate': np.random.uniform(90, 99),
                'Training Hours': np.random.randint(8, 16),
                'Specializations': np.random.choice(['General', 'Cardiology', 'Orthopedics'], 1)[0]
            })
        
        # Generate data for Saqib Sherwani team
        for scribe in saqib_team:
            all_scribes.append({
                'Scribe Name': scribe,
                'Team Leader': 'Saqib Sherwani',
                'Monthly Patients': np.random.randint(55, 115),
                'Efficiency Score': np.random.uniform(88, 99),
                'Avg Session Length': np.random.uniform(2.3, 4.2),
                'Provider Rating': np.random.uniform(4.2, 5.0),
                'Attendance Rate': np.random.uniform(92, 99),
                'Training Hours': np.random.randint(10, 18),
                'Specializations': np.random.choice(['General', 'Cardiology', 'Orthopedics', 'Emergency'], 1)[0]
            })
        
        return pd.DataFrame(all_scribes)
    
    def _generate_patient_count_data(self) -> pd.DataFrame:
        """Generate patient count data"""
        providers = [
            "Dr. Mark Basham", "Amanda DeBois", "Melanie Arrington", "Alison Blake", "Nikki Kelly",
            "Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Lisa Rodriguez", "Dr. James Wilson",
            "Dr. Emily Davis", "Dr. Robert Taylor", "Dr. Jennifer Martinez", "Dr. David Anderson"
        ]
        
        patient_data = []
        for provider in providers:
            for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']:
                patient_data.append({
                    'Provider': provider,
                    'Month': month,
                    'Patient Count': np.random.randint(60, 150),
                    'Avg Session Duration': np.random.uniform(2.0, 4.5),
                    'Assigned Scribe': np.random.choice([
                        'Nikhil Yadav', 'Prachi Sharma', 'Muskan Gupta', 'Anmol Agarwal'
                    ])
                })
        
        return pd.DataFrame(patient_data)
    
    def _generate_utilization_data(self) -> pd.DataFrame:
        """Generate utilization data"""
        scribes = ['Nikhil Yadav', 'Prachi Sharma', 'Ayushi Singh', 'Muskan Gupta', 'Anmol Agarwal']
        
        utilization_data = []
        for scribe in scribes:
            for week in range(1, 5):  # 4 weeks
                utilization_data.append({
                    'Scribe': scribe,
                    'Week': f'Week {week}',
                    'Hours Worked': np.random.uniform(30, 45),
                    'Utilization Rate': np.random.uniform(75, 95),
                    'Peak Hours Coverage': np.random.uniform(85, 98),
                    'Weekend Availability': np.random.choice([True, False], p=[0.7, 0.3])
                })
        
        return pd.DataFrame(utilization_data)
    
    def _generate_monthly_data(self, month: str) -> pd.DataFrame:
        """Generate monthly activity data"""
        dates = pd.date_range(
            start=f'2024-{["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"].index(month) + 1:02d}-01',
            end=f'2024-{["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"].index(month) + 1:02d}-28',
            freq='D'
        )
        
        monthly_data = []
        for date in dates:
            # Generate 5-15 sessions per day
            num_sessions = np.random.randint(5, 16)
            
            for _ in range(num_sessions):
                monthly_data.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Scribe': np.random.choice([
                        'Nikhil Yadav', 'Prachi Sharma', 'Ayushi Singh', 'Rohan Setia',
                        'Muskan Gupta', 'Anmol Agarwal', 'Shreya Jain', 'Vineet Kumar'
                    ]),
                    'Provider': np.random.choice([
                        'Dr. Mark Basham', 'Amanda DeBois', 'Melanie Arrington', 
                        'Dr. Sarah Johnson', 'Alison Blake'
                    ]),
                    'Start Time': f"{np.random.randint(8, 17)}:{np.random.randint(0, 59):02d}",
                    'End Time': f"{np.random.randint(9, 18)}:{np.random.randint(0, 59):02d}",
                    'Patient Count': np.random.randint(1, 8),
                    'Session Rating': np.random.uniform(4.0, 5.0)
                })
        
        return pd.DataFrame(monthly_data)
    
    def refresh_cache(self):
        """Clear all cached data to force refresh"""
        self.cache.clear()
        logger.info("Data cache cleared successfully")
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get connection status and diagnostics"""
        status = 'Connected' if st.session_state.get('sheets_connected') else 'Sample Data'
        return {
            'status': status,
            'spreadsheet_id': self.spreadsheet_id,
            'cache_entries': len(self.cache),
            'last_update': datetime.now().strftime('%H:%M:%S'),
            'rate_limit_status': 'Normal'
        }


def get_sheets_connector() -> GoogleSheetsConnector:
    """Get or create Google Sheets connector instance"""
    if 'sheets_connector' not in st.session_state:
        spreadsheet_id = "17SFltoaYiEVVHDN7flctrHn1TKj01xCCyrsoiCN7L8c"
        st.session_state.sheets_connector = GoogleSheetsConnector(spreadsheet_id)
    
    return st.session_state.sheets_connector


def load_all_data() -> Dict[str, pd.DataFrame]:
    """Load all data from Google Sheets"""
    connector = get_sheets_connector()
    return connector.get_all_sheets()


def refresh_data():
    """Refresh all cached data"""
    connector = get_sheets_connector()
    connector.refresh_cache()


def get_data_status() -> Dict[str, Any]:
    """Get current data connection status"""
    connector = get_sheets_connector()
    return connector.get_connection_status()
