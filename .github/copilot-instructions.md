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

### Technical Requirements

#### Data Architecture
- **Real-time Sync**: Auto-refresh every 5-10 minutes
- **Caching Strategy**: Smart caching to minimize API calls
- **Error Handling**: Graceful degradation when API limits hit
- **Data Validation**: Ensure data integrity and consistency

#### UI/UX Requirements
- **Professional Design**: Modern, clean, business-appropriate
- **Responsive Layout**: Works on desktop, tablet, mobile
- **Interactive Elements**: Filters, drill-downs, hover details
- **Export Capabilities**: PDF reports, CSV data exports
- **Theme Options**: Dark/light mode toggle

#### Performance Requirements
- **Fast Loading**: < 3 seconds initial load
- **Smooth Interactions**: No lag in filtering/navigation
- **Efficient Data Processing**: Optimized pandas operations
- **Memory Management**: Handle large datasets efficiently

## Technical Stack

### Core Technologies
- **Streamlit**: Main dashboard framework
- **Google Sheets API**: Data source integration
- **Pandas**: Data processing and analysis
- **Plotly**: Interactive charts and visualizations
- **Altair**: Additional charting options

### Supporting Libraries
- **streamlit-autorefresh**: Auto-refresh functionality
- **streamlit-aggrid**: Advanced data grids
- **plotly-dash**: Enhanced interactivity
- **google-auth**: Authentication handling
- **cachetools**: Advanced caching strategies

## Project Structure

```
ScribeDash/
├── .github/
│   └── instructions                # This file
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py              # Navigation and filters
│   │   ├── overview.py             # Executive dashboard
│   │   ├── team_performance.py     # Team metrics
│   │   ├── individual_metrics.py   # Individual scribe analysis
│   │   ├── provider_analysis.py    # Provider insights
│   │   ├── realtime_activity.py    # Live monitoring
│   │   └── trends_analytics.py     # Trends and forecasting
│   ├── data/
│   │   ├── __init__.py
│   │   ├── google_sheets.py        # Google Sheets API integration
│   │   ├── data_processor.py       # Data transformation logic
│   │   └── cache_manager.py        # Caching and refresh logic
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py               # Configuration management
│   │   ├── helpers.py              # Utility functions
│   │   └── styles.py               # CSS and styling
│   └── main.py                     # Main Streamlit app
├── config/
│   ├── settings.py                 # App configuration
│   └── credentials.json.example    # Google API credentials template
├── requirements.txt                # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── README.md                      # End-user documentation
└── run.sh                         # Deployment script
```

## Data Models and Key Metrics

### Scribe Performance Metrics
- **Patient Count**: Monthly patient notes processed
- **Efficiency Score**: Patient count / Hours worked
- **Utilization Rate**: Active hours / Total scheduled hours
- **Quality Score**: Based on feedback and accuracy
- **Consistency Score**: Variance in daily performance

### Team Performance Metrics
- **Team Productivity**: Combined team output
- **Coverage Reliability**: Backup coverage success rate
- **Team Efficiency**: Average efficiency across team members
- **Workload Balance**: Standard deviation of assignments

### Provider Satisfaction Metrics
- **Response Time**: Time to complete assignments
- **Availability**: Coverage percentage
- **Quality Rating**: Provider feedback scores
- **Stability**: Assignment consistency over time

## API Integration Guidelines

### Google Sheets API
- **Rate Limiting**: Respect 60 requests/minute limit
- **Batch Operations**: Group API calls efficiently
- **Error Handling**: Implement retry logic with exponential backoff
- **Authentication**: Use service account credentials

### Data Refresh Strategy
- **Incremental Updates**: Only fetch changed data when possible
- **Smart Caching**: Cache data with appropriate TTL
- **Background Refresh**: Update data without blocking UI
- **Conflict Resolution**: Handle concurrent data modifications

## Deployment and Maintenance

### Deployment Options
1. **Streamlit Cloud**: Easiest deployment option
2. **Heroku**: More control and custom domain
3. **AWS/GCP**: Enterprise-grade deployment
4. **Local Network**: Internal company deployment

### Monitoring and Alerts
- **API Usage Monitoring**: Track quota consumption
- **Performance Metrics**: Response time tracking
- **Error Logging**: Comprehensive error tracking
- **Uptime Monitoring**: Service availability alerts

### Security Considerations
- **Credential Management**: Secure storage of API keys
- **Access Control**: User authentication if needed
- **Data Privacy**: Protect sensitive information
- **Audit Logging**: Track data access and modifications

## Development Guidelines

### Code Standards
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations throughout
- **Documentation**: Comprehensive docstrings
- **Testing**: Unit tests for critical functions

### Git Workflow
- **Feature Branches**: Develop features in separate branches
- **Code Review**: Peer review before merging
- **Commit Messages**: Clear, descriptive commit messages
- **Version Tags**: Tag releases for tracking

### Performance Optimization
- **Data Caching**: Implement multi-level caching
- **Lazy Loading**: Load data only when needed
- **Memory Efficiency**: Optimize pandas operations
- **UI Responsiveness**: Use async operations where possible

## Future Enhancements

### Phase 2 Features
- **Mobile App**: React Native or Flutter app
- **Advanced Analytics**: Machine learning insights
- **Automated Reporting**: Scheduled PDF reports
- **Integration APIs**: Connect with EHR systems

### Scalability Considerations
- **Database Migration**: Move from Sheets to proper database
- **Microservices**: Break into smaller services
- **Load Balancing**: Handle increased user load
- **Real-time Notifications**: WebSocket-based alerts

## Support and Maintenance

### Regular Maintenance Tasks
- **Data Validation**: Weekly data integrity checks
- **Performance Review**: Monthly performance analysis
- **Security Updates**: Regular dependency updates
- **User Feedback**: Continuous improvement based on feedback

### Troubleshooting Guide
- **API Errors**: Common Google Sheets API issues
- **Performance Issues**: Optimization strategies
- **Data Inconsistencies**: Resolution procedures
- **Deployment Problems**: Common deployment fixes

## Contact and Escalation

### Key Stakeholders
- **Project Owner**: Saqib Sherwani
- **Technical Lead**: [To be assigned]
- **End Users**: Management and team leaders

### Escalation Process
1. **Technical Issues**: Check logs and error messages
2. **Data Issues**: Verify Google Sheets integrity
3. **Performance Issues**: Review caching and optimization
4. **Business Logic**: Consult with stakeholders

---

**Last Updated**: August 25, 2025
**Version**: 1.0
**Maintainer**: Development Team