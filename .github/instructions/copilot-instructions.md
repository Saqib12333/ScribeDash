# ScribeDash - Medical Scribing Dashboard Instructions

## Project Overview

ScribeDash is a real-time Streamlit dashboard for monitoring and managing medical scribing operations. The dashboard connects to a Google Spreadsheet to provide live insights into scribe performance, provider assignments, patient counts, and operational metrics for a remote medical scribing company.

## Business Context

### Company Structure
- **Remote Medical Scribing Company** providing services to healthcare providers
- **Two Team Leaders**: Haider Khan and Saqib Sherwani
- **38 Scribes** assigned to various healthcare providers and clients
- **Daily Operations** tracked through Google Sheets with real-time updates

### Scribes Team
```
Shivam Chauhan, Sutirtha Chakraborty, Ansika Negi, Prachi Sharma, 
Prarthana Sinha Roy, Akshita Pandey, Rohan Setia, Nikhil Yadav, 
Vaibhavi Mittal, Ayushi Singh, Deepa Deepak, Tenzin Wangmo, 
Piyush Sharma, Debraj Dey, Priyanka Bhadauria, Solomon Raju, 
Rozy Chugh, Ashutosh Srivastava, Manvitha Gullipalli, 
Samir Bhattacharya, Pankaj Kumar Singh, Amisha Raj, Navya Dwivedi, 
Puja Agarwal, Dhriti Shukla, Bijaya Biswas, Devansh Sharma, 
Pragya Pal, Vaydoorya, Deepak Devasia, Iqra Khan, Bithika Maji, 
Bagmita Borah, Ayushi Aggarwal, Amandeep Chauhan, Sakshi Sharma, 
Suruchi Bhatia, Sarthak Kapoor
```

### Key Providers & Clients
```
PROVIDER → CLIENT
Erin Henderson → Alliance Pain Center
Kei Batangan → Alliance Pain Center
Dr. Christine Potterjones → Battle Mountain General Hospital
Dr. Kaleb Wartgow → South Lyon Medical Center
Dr. Kirmani Moe → Collaborative Solutions in Psychiatry
Dr. Mark Basham → Greenwood County Hospital
Alison Blake → Revitalize Medical Solutions
Amanda DeBois → Revitalize Medical Solutions
Heather Reynolds → Revitalize Medical Solutions
[... and many more]
```

## Google Spreadsheet Structure

**Main Spreadsheet ID**: `17SFltoaYiEVVHDN7flctrHn1TKj01xCCyrsoiCN7L8c`

### Key Sheets:

1. **Dataset Sheet**
   - Scribe assignments and team structure
   - Provider mappings
   - Task definitions
   - Shift information (IST/CST)

2. **Patient Count Sheet**
   - Monthly patient note counts by scribe
   - Performance tracking (Jan-Aug 2025)
   - Average calculations
   - Performance metrics

3. **Utilization Sheet**
   - Scribe utilization rates
   - Efficiency metrics
   - Resource allocation data

4. **Monthly Activity Sheets** (January - August)
   - Daily activity logs
   - Task assignments
   - Hours tracking (Scribe hours vs Provider hours)
   - Schedule adherence
   - Patient scheduling data
   - Comments and notes

5. **Credentials Sheet** (Hidden)
   - System access information
   - Zoom credentials
   - EHR login details

## Dashboard Requirements

### Target Audience
- **Primary**: Management/Boss - needs professional, smooth, attractive, presentable interface
- **Secondary**: Team leaders and operations staff

### Core Features

#### 1. Executive Overview Dashboard
- **Key Metrics Cards**: Total scribes, active providers, monthly stats
- **Team Performance Comparison**: Haider Khan vs Saqib Sherwani teams
- **Current Month Progress**: Real-time progress indicators
- **Quick Stats**: Patient counts, utilization rates, efficiency metrics

#### 2. Team Performance Analysis
- **Team Breakdown**: Performance by team leader
- **Scribe Performance Rankings**: Top performers, improvement needed
- **Provider Coverage**: Assignment stability and coverage patterns
- **Workload Distribution**: Balanced assignments analysis

#### 3. Individual Scribe Metrics
- **Detailed Performance**: Individual scribe deep-dive
- **Patient Count Trends**: Monthly progression charts
- **Efficiency Analysis**: Hours worked vs output
- **Assignment History**: Provider relationships over time

#### 4. Provider & Client Analysis
- **Provider Utilization**: Usage patterns and efficiency
- **Client Satisfaction Metrics**: Performance by client
- **Coverage Analytics**: Backup coverage patterns
- **Assignment Stability**: Provider-scribe relationship duration

#### 5. Real-time Activity Monitor
- **Live Status Dashboard**: Current day activities
- **Schedule Adherence**: On-time performance
- **Task Completion**: Real-time progress tracking
- **Alert System**: Issues requiring attention

#### 6. Trends & Predictive Analytics
- **Monthly Comparisons**: Performance trends over time
- **Seasonal Patterns**: Workload variations
- **Forecasting**: Predictive analytics for resource planning
- **Bottleneck Identification**: Process improvement opportunities

