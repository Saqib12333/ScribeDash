"""
Data processing utilities for ScribeDash
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import streamlit as st


class DataProcessor:
    """Data processing and analytics engine"""
    
    def __init__(self, raw_data: Dict[str, pd.DataFrame]):
        self.raw_data = raw_data
        self.processed_data = {}
        self._process_all_data()
    
    def _process_all_data(self):
        """Process all raw data into analytics-ready format"""
        try:
            self.processed_data['scribes'] = self._process_scribe_data()
            self.processed_data['providers'] = self._process_provider_data()
            self.processed_data['sessions'] = self._process_session_data()
            self.processed_data['metrics'] = self._calculate_metrics()
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
    
    def _process_scribe_data(self) -> pd.DataFrame:
        """Process scribe performance data"""
        if 'Dataset' not in self.raw_data or self.raw_data['Dataset'].empty:
            return pd.DataFrame()
        
        df = self.raw_data['Dataset'].copy()
        
        # Clean and standardize data
        for col, fallback in [
            ('Efficiency Score', None),
            ('Monthly Patients', 0),
            ('Avg Session Length', None),
            ('Provider Rating', None),
            ('Attendance Rate', None),
            ('Training Hours', None),
            ('Team Leader', 'Unknown')
        ]:
            if col not in df.columns:
                df[col] = fallback
        
        for col in ['Efficiency Score', 'Monthly Patients', 'Avg Session Length', 'Provider Rating', 'Attendance Rate']:
            if col in df.columns:
                df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
        
        # Add derived metrics
        if 'Efficiency Score' in df.columns:
            df['Performance Category'] = df['Efficiency Score'].apply(self._categorize_performance)
        if 'Monthly Patients' in df.columns:
            df['Workload Category'] = df['Monthly Patients'].apply(self._categorize_workload)
        if 'Training Hours' in df.columns:
            df['Experience Level'] = df['Training Hours'].apply(self._categorize_experience)
        
        # Add team statistics
        team_col = 'Team Leader' if 'Team Leader' in df.columns else None
        if team_col:
            team_stats = df.groupby(team_col).agg({
            'Efficiency Score': 'mean',
            'Monthly Patients': 'sum',
            'Provider Rating': 'mean'
        }).add_suffix('_Team_Avg')
            df = df.merge(team_stats, left_on=team_col, right_index=True, how='left')
        
        return df
    
    def _process_provider_data(self) -> pd.DataFrame:
        """Process provider assignment and performance data"""
        if 'Patient Count' not in self.raw_data or self.raw_data['Patient Count'].empty:
            return pd.DataFrame()
        
        df = self.raw_data['Patient Count'].copy()
        
        # Clean data
        df['Patient Count'] = pd.to_numeric(df['Patient Count'], errors='coerce')
        df['Avg Session Duration'] = pd.to_numeric(df['Avg Session Duration'], errors='coerce')
        
        # Calculate provider statistics
        provider_stats = df.groupby('Provider').agg({
            'Patient Count': ['sum', 'mean', 'std'],
            'Avg Session Duration': 'mean'
        }).round(2)
        
        # Flatten column names
        provider_stats.columns = ['_'.join(col).strip() for col in provider_stats.columns]
        provider_stats = provider_stats.reset_index()
        
        # Add efficiency metrics
        provider_stats['Consistency_Score'] = (
            100 - (provider_stats['Patient Count_std'] / provider_stats['Patient Count_mean'] * 100)
        ).fillna(100)
        
        return provider_stats
    
    def _process_session_data(self) -> pd.DataFrame:
        """Process session data from monthly sheets"""
        # Use actual available monthly sheets
        monthly_sheets = ['August', 'July', 'May', 'February', 'January']
        
        all_sessions = []
        for month in monthly_sheets:
            if month in self.raw_data and not self.raw_data[month].empty:
                month_data = self.raw_data[month].copy()
                month_data['Month'] = month
                all_sessions.append(month_data)
        
        if not all_sessions:
            # If no monthly data, try to use current month data (August)
            if 'August' in self.raw_data and not self.raw_data['August'].empty:
                df = self.raw_data['August'].copy()
                df['Month'] = 'August'
                return self._process_monthly_data(df)
            return pd.DataFrame()
        
        df = pd.concat(all_sessions, ignore_index=True)
        return self._process_monthly_data(df)
    
    def _process_monthly_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process monthly data with flexible column handling"""
        if df.empty:
            return df
        
        # Debug: Print available columns
        print(f"Available columns: {list(df.columns)}")
        
        # Try to identify and clean common columns
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        patient_cols = [col for col in df.columns if 'patient' in col.lower()]
        time_cols = [col for col in df.columns if 'time' in col.lower()]
        rating_cols = [col for col in df.columns if 'rating' in col.lower()]
        
        # Process available data flexibly
        if date_cols:
            df['Date'] = pd.to_datetime(df[date_cols[0]], errors='coerce')
        
        if patient_cols:
            df['Patient Count'] = pd.to_numeric(df[patient_cols[0]], errors='coerce')
        
        if rating_cols:
            df['Session Rating'] = pd.to_numeric(df[rating_cols[0]], errors='coerce')
        
        # Handle time columns if available
        start_time_col = next((col for col in time_cols if 'start' in col.lower()), None)
        end_time_col = next((col for col in time_cols if 'end' in col.lower()), None)
        
        if start_time_col and end_time_col:
            df['Start Time'] = df[start_time_col]
            df['End Time'] = df[end_time_col]
            df['Duration_Hours'] = self._calculate_session_duration(df['Start Time'], df['End Time'])
        
        # Add time-based features if date is available
        if 'Date' in df.columns and not df['Date'].isna().all():
            df['Day_of_Week'] = df['Date'].dt.day_name()
            df['Week_of_Year'] = df['Date'].dt.isocalendar().week
        
        # Add derived columns
        if 'Session Rating' in df.columns:
            df['Rating_Category'] = df['Session Rating'].apply(self._categorize_rating)
        
        if start_time_col:
            try:
                df['Hour'] = pd.to_datetime(df[start_time_col], format='%H:%M', errors='coerce').dt.hour
                df['Time_Category'] = df['Hour'].apply(self._categorize_time)
            except:
                pass
        
        return df
    
    def _calculate_session_duration(self, start_times: pd.Series, end_times: pd.Series) -> pd.Series:
        """Calculate session duration in hours"""
        durations = []
        
        for start, end in zip(start_times, end_times):
            try:
                start_time = pd.to_datetime(start, format='%H:%M')
                end_time = pd.to_datetime(end, format='%H:%M')
                
                # Handle sessions that cross midnight
                if end_time < start_time:
                    end_time += timedelta(days=1)
                
                duration = (end_time - start_time).total_seconds() / 3600
                durations.append(duration)
            except:
                durations.append(np.nan)
        
        return pd.Series(durations)
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate key performance metrics"""
        metrics = {}
        
        # Overall metrics
        if 'scribes' in self.processed_data and not self.processed_data['scribes'].empty:
            scribe_df = self.processed_data['scribes']
            
            metrics['total_scribes'] = len(scribe_df)
            metrics['avg_efficiency'] = scribe_df['Efficiency Score'].mean()
            metrics['total_monthly_patients'] = scribe_df['Monthly Patients'].sum()
            metrics['avg_provider_rating'] = scribe_df['Provider Rating'].mean()
            
            # Team metrics
            metrics['team_comparison'] = scribe_df.groupby('Team Leader').agg({
                'Efficiency Score': 'mean',
                'Monthly Patients': 'sum',
                'Provider Rating': 'mean'
            }).round(2).to_dict()
        
        # Session metrics
        if 'sessions' in self.processed_data and not self.processed_data['sessions'].empty:
            session_df = self.processed_data['sessions']
            
            metrics['total_sessions'] = len(session_df)
            metrics['avg_session_duration'] = session_df['Duration_Hours'].mean()
            metrics['avg_session_rating'] = session_df['Session Rating'].mean()
            
            # Time-based metrics
            metrics['peak_hours_efficiency'] = session_df[
                session_df['Time_Category'] == 'Peak'
            ]['Session Rating'].mean()
            
            metrics['weekend_coverage'] = len(session_df[
                session_df['Day_of_Week'].isin(['Saturday', 'Sunday'])
            ]) / len(session_df) * 100
        
        # Provider metrics
        if 'providers' in self.processed_data and not self.processed_data['providers'].empty:
            provider_df = self.processed_data['providers']
            
            metrics['total_providers'] = len(provider_df)
            metrics['avg_patients_per_provider'] = provider_df['Patient Count_mean'].mean()
        
        return metrics
    
    def _categorize_performance(self, efficiency: float) -> str:
        """Categorize scribe performance"""
        if pd.isna(efficiency):
            return 'Unknown'
        elif efficiency >= 95:
            return 'Excellent'
        elif efficiency >= 90:
            return 'Good'
        elif efficiency >= 80:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    def _categorize_workload(self, patients: int) -> str:
        """Categorize scribe workload"""
        if pd.isna(patients):
            return 'Unknown'
        elif patients >= 100:
            return 'High'
        elif patients >= 70:
            return 'Medium'
        else:
            return 'Low'
    
    def _categorize_experience(self, training_hours: int) -> str:
        """Categorize scribe experience level"""
        if pd.isna(training_hours):
            return 'Unknown'
        elif training_hours >= 15:
            return 'Senior'
        elif training_hours >= 10:
            return 'Intermediate'
        else:
            return 'Junior'
    
    def _categorize_rating(self, rating: float) -> str:
        """Categorize session rating"""
        if pd.isna(rating):
            return 'Unknown'
        elif rating >= 4.5:
            return 'Excellent'
        elif rating >= 4.0:
            return 'Good'
        elif rating >= 3.5:
            return 'Fair'
        else:
            return 'Poor'
    
    def _categorize_time(self, hour: int) -> str:
        """Categorize time of day"""
        if pd.isna(hour):
            return 'Unknown'
        elif 10 <= hour <= 14:
            return 'Peak'
        elif 8 <= hour <= 18:
            return 'Standard'
        else:
            return 'Off-Hours'
    
    def get_scribe_performance(self, scribe_name: Optional[str] = None) -> pd.DataFrame:
        """Get performance data for specific scribe or all scribes"""
        if 'scribes' not in self.processed_data:
            return pd.DataFrame()
        
        df = self.processed_data['scribes']
        
        if scribe_name:
            return df[df['Scribe Name'] == scribe_name]
        
        return df
    
    def get_team_comparison(self) -> Dict[str, Any]:
        """Get team comparison metrics"""
        if 'metrics' not in self.processed_data:
            return {}
        
        return self.processed_data['metrics'].get('team_comparison', {})
    
    def get_provider_analysis(self, provider_name: Optional[str] = None) -> pd.DataFrame:
        """Get provider analysis data"""
        if 'providers' not in self.processed_data:
            return pd.DataFrame()
        
        df = self.processed_data['providers']
        
        if provider_name:
            return df[df['Provider'] == provider_name]
        
        return df
    
    def get_session_trends(self, period: str = 'monthly') -> pd.DataFrame:
        """Get session trend data"""
        if 'sessions' not in self.processed_data:
            return pd.DataFrame()
        
        df = self.processed_data['sessions']
        
        if period == 'monthly':
            return df.groupby('Month').agg({
                'Patient Count': 'sum',
                'Session Rating': 'mean',
                'Duration_Hours': 'mean'
            }).round(2)
        elif period == 'weekly':
            return df.groupby('Week_of_Year').agg({
                'Patient Count': 'sum',
                'Session Rating': 'mean',
                'Duration_Hours': 'mean'
            }).round(2)
        elif period == 'daily':
            return df.groupby('Day_of_Week').agg({
                'Patient Count': 'sum',
                'Session Rating': 'mean',
                'Duration_Hours': 'mean'
            }).round(2)
        
        return df
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get current real-time metrics"""
        current_time = datetime.now()
        
        # Simulate real-time data
        metrics = {
            'active_sessions': np.random.randint(15, 25),
            'sessions_today': np.random.randint(45, 65),
            'current_efficiency': np.random.uniform(88, 96),
            'alerts_count': np.random.randint(0, 5),
            'last_update': current_time.strftime('%H:%M:%S')
        }
        
        return metrics
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get comprehensive summary statistics"""
        if 'metrics' not in self.processed_data:
            return {}
        
        return self.processed_data['metrics']


def process_data(raw_data: Dict[str, pd.DataFrame]) -> DataProcessor:
    """Process raw data and return analytics engine"""
    return DataProcessor(raw_data)


def calculate_kpis(data_processor: DataProcessor) -> Dict[str, Any]:
    """Calculate key performance indicators"""
    return data_processor.get_summary_stats()


def get_trend_analysis(data_processor: DataProcessor, period: str = 'monthly') -> pd.DataFrame:
    """Get trend analysis for specified period"""
    return data_processor.get_session_trends(period)
