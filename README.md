# ScribeDash - Real-Time Medical Scribing Dashboard

<div align="center">
  
  ![ScribeDash Logo](https://img.shields.io/badge/ScribeDash-Medical%20Dashboard-blue?style=for-the-badge)
  
  **Professional real-time dashboard for medical scribing operations management**
  
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python&logoColor=white)](https://python.org/)
  [![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=flat&logo=googlesheets&logoColor=white)](https://sheets.google.com/)
  
</div>

## 🏥 Overview

ScribeDash is a comprehensive, real-time dashboard designed specifically for monitoring and managing medical scribing operations. It provides live insights into scribe performance, provider assignments, patient counts, and operational metrics, helping management make data-driven decisions to optimize their remote medical scribing company.

### 🎯 Key Features

- **📊 Real-Time Analytics**: Live data updates from Google Sheets every 5-10 minutes
- **👥 Team Management**: Track performance across different team leaders (Haider Khan & Saqib Sherwani)
- **📈 Performance Metrics**: Individual scribe performance tracking and trending
- **🏥 Provider Analysis**: Client and provider utilization insights
- **⚡ Live Monitoring**: Current day activity tracking and alerts
- **📋 Executive Reports**: Professional dashboards for management review

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Sheets API credentials
- Internet connection for real-time data access

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ScribeDash
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets API**
   - Create a Google Cloud Project
   - Enable Google Sheets API
   - Download service account credentials
   - Place credentials in `config/credentials.json`

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the dashboard**
   ```bash
   streamlit run src/main.py
   ```

The dashboard will be available at `http://localhost:8501`

## 📊 Dashboard Sections

### 🏢 Executive Overview
- **Key Performance Indicators**: Total scribes, active providers, monthly statistics
- **Team Comparison**: Haider Khan vs Saqib Sherwani team performance
- **Current Month Progress**: Real-time progress tracking
- **Quick Insights**: Patient counts, utilization rates, efficiency metrics

### 👥 Team Performance
- **Team Leader Analytics**: Detailed breakdown by team leader
- **Scribe Rankings**: Top performers and improvement opportunities  
- **Workload Distribution**: Balanced assignment analysis
- **Coverage Patterns**: Provider assignment stability

### 🧑‍⚕️ Individual Metrics
- **Scribe Deep-Dive**: Detailed individual performance analysis
- **Trend Analysis**: Monthly progression and patterns
- **Efficiency Tracking**: Hours worked vs patient output ratios
- **Assignment History**: Provider relationship tracking over time

### 🏥 Provider Analysis
- **Utilization Rates**: Provider usage patterns and efficiency
- **Client Performance**: Satisfaction metrics by healthcare client
- **Coverage Analytics**: Backup coverage success rates
- **Relationship Stability**: Long-term provider-scribe partnerships

### ⚡ Real-Time Activity
- **Live Status Monitor**: Current day activities and progress
- **Schedule Adherence**: Real-time attendance and punctuality tracking
- **Task Completion**: Live progress on daily assignments
- **Alert Dashboard**: Issues requiring immediate attention

### 📈 Trends & Analytics
- **Historical Analysis**: Month-over-month comparisons
- **Performance Forecasting**: Predictive analytics for resource planning
- **Seasonal Patterns**: Workload variation insights
- **Process Optimization**: Bottleneck identification and recommendations

## 📋 Data Sources

The dashboard integrates with a comprehensive Google Spreadsheet containing:

- **38 Medical Scribes** across two teams
- **40+ Healthcare Providers** and their respective clients
- **Daily Activity Logs** with detailed task tracking
- **Monthly Performance Data** (January - August 2025)
- **Utilization Metrics** and efficiency calculations

### Key Metrics Tracked

| Metric Category | Examples |
|---|---|
| **Performance** | Patient counts, efficiency scores, quality ratings |
| **Utilization** | Active hours, scheduled hours, availability rates |
| **Assignments** | Provider relationships, client coverage, backup duties |
| **Trends** | Monthly comparisons, seasonal patterns, growth trajectories |

## 🎨 User Interface

### Design Principles
- **Professional**: Clean, business-appropriate interface suitable for executive review
- **Intuitive**: Easy navigation with clear information hierarchy
- **Responsive**: Optimized for desktop, tablet, and mobile viewing
- **Interactive**: Drill-down capabilities, filtering, and real-time updates

### Navigation
- **Sidebar Navigation**: Quick access to all dashboard sections
- **Interactive Filters**: Date ranges, team selection, individual scribe focus
- **Export Options**: PDF reports and CSV data downloads
- **Theme Toggle**: Light and dark mode options

## 🔧 Configuration

### Environment Variables
```bash
# Google Sheets Configuration
GOOGLE_SHEETS_ID=17SFltoaYiEVVHDN7flctrHn1TKj01xCCyrsoiCN7L8c
GOOGLE_CREDENTIALS_PATH=config/credentials.json

# Dashboard Settings
REFRESH_INTERVAL=300  # 5 minutes
CACHE_TTL=600        # 10 minutes
DEBUG_MODE=False

# UI Configuration
DEFAULT_THEME=light
SHOW_RAW_DATA=False
ENABLE_EXPORTS=True
```

### Google Sheets API Setup

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing one

2. **Enable APIs**
   - Enable Google Sheets API
   - Enable Google Drive API (if needed)

3. **Create Service Account**
   - Create service account with appropriate permissions
   - Download JSON credentials file
   - Share your Google Sheet with the service account email

4. **Configure Permissions**
   - Ensure service account has read access to the spreadsheet
   - Verify API quotas are sufficient for your usage

## 📱 Deployment Options

### 🌐 Streamlit Cloud (Recommended)
- **Easy Setup**: Direct deployment from GitHub
- **Automatic Updates**: Continuous deployment on code changes
- **Free Tier Available**: Cost-effective for small teams
- **Custom Domain**: Professional URL branding

### 🚀 Heroku
- **Scalable**: Easy scaling as usage grows
- **Custom Domain**: Professional branding options
- **Add-ons**: Database and monitoring integrations
- **Continuous Deployment**: GitHub integration

### ☁️ Cloud Platforms (AWS/GCP/Azure)
- **Enterprise Grade**: High availability and security
- **Custom Infrastructure**: Full control over deployment
- **Advanced Monitoring**: Comprehensive logging and alerts
- **Compliance**: Healthcare data security requirements

### 🏢 Local Network Deployment
- **Security**: Complete data control within organization
- **Performance**: Reduced latency for internal users
- **Customization**: Full environment control
- **Compliance**: Meet specific regulatory requirements

## 🔒 Security & Privacy

### Data Protection
- **Secure API Access**: Service account authentication
- **Encrypted Transmission**: HTTPS for all data transfers
- **Access Control**: Role-based permissions
- **Audit Logging**: Comprehensive access tracking

### Privacy Considerations
- **Minimal Data Storage**: Cache only necessary data temporarily
- **No Sensitive Data**: Credentials and personal info handled securely
- **Compliance Ready**: HIPAA-friendly architecture
- **Data Retention**: Configurable cache expiration policies

## 🛠️ Troubleshooting

### Common Issues

#### **Dashboard Not Loading**
- Check internet connection
- Verify Google Sheets API credentials
- Confirm spreadsheet sharing permissions
- Check Streamlit logs for errors

#### **Data Not Updating**
- Verify API quota limits (60 requests/minute)
- Check cache settings and TTL values
- Confirm Google Sheets accessibility
- Review error logs for API failures

#### **Performance Issues**
- Monitor memory usage with large datasets
- Optimize cache settings
- Check network connectivity
- Review Google Sheets API response times

#### **Display Issues**
- Clear browser cache
- Try incognito/private browsing mode
- Check for browser compatibility
- Verify responsive layout on different screen sizes

### Getting Help

1. **Check Logs**: Review Streamlit console output
2. **Verify Configuration**: Confirm all environment variables
3. **Test API Access**: Manually verify Google Sheets connectivity
4. **Review Documentation**: Check `.github/instructions` for detailed technical info

## 📈 Performance Optimization

### Best Practices
- **Smart Caching**: Implement multi-level caching strategy
- **Efficient Queries**: Minimize Google Sheets API calls
- **Data Processing**: Optimize pandas operations
- **UI Responsiveness**: Use async operations where possible

### Monitoring
- **API Usage**: Track quota consumption
- **Response Times**: Monitor dashboard performance
- **Error Rates**: Alert on failures
- **User Experience**: Track page load times

## 🔄 Updates & Maintenance

### Regular Tasks
- **Weekly**: Data integrity verification
- **Monthly**: Performance review and optimization
- **Quarterly**: Security updates and dependency upgrades
- **As Needed**: Feature enhancements based on user feedback

### Backup & Recovery
- **Configuration Backup**: Version control for all settings
- **Data Recovery**: Google Sheets provides built-in versioning
- **Deployment Rollback**: Quick reversion to previous versions
- **Disaster Recovery**: Multi-environment deployment strategy

## 🤝 Support

### Contact Information
- **Project Owner**: Saqib Sherwani
- **Technical Support**: Development Team
- **Business Questions**: Management Team

### Support Process
1. **Documentation**: Check this README and technical instructions
2. **Self-Service**: Use troubleshooting guide
3. **Technical Issues**: Contact development team
4. **Business Requirements**: Reach out to project stakeholders

## 📄 License

This project is proprietary software developed for internal use by the medical scribing company. All rights reserved.

---

<div align="center">
  
  **Built with ❤️ for medical scribing excellence**
  
  Last Updated: August 25, 2025 | Version 1.0
  
</div>
