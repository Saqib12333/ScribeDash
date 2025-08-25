# ScribeDash Installation & Setup Guide

## Quick Start

### 1. Install Dependencies

First, navigate to the project directory and install the required packages:

```powershell
cd "C:\Users\sherw\OneDrive\Documents\App Projects\Others\ScribeDash"
pip install -r requirements.txt
```

### 2. Run the Application

Launch the dashboard using Streamlit:

```powershell
streamlit run src/main.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Features Overview

### 📊 Executive Overview
- Key performance metrics at a glance
- Team comparison charts
- Monthly trends and patterns
- Real-time status indicators

### 👥 Team Performance
- Detailed team analytics for Haider Khan and Saqib Sherwani teams
- Efficiency trends and workload distribution
- Performance rankings and attendance patterns
- Comprehensive team comparison metrics

### 👤 Individual Metrics
- Individual scribe performance analysis
- Efficiency timelines and workload patterns
- Provider compatibility scores
- Goals and recommendations for each scribe

### 🩺 Provider Analysis
- Provider-specific insights and metrics
- Scribe assignment history and performance
- Session patterns and utilization analysis
- Provider satisfaction scores

### ⚡ Real-time Activity
- Live monitoring of active sessions
- Recent completions and current status
- Auto-refresh capabilities
- Alert notifications and system health

### 📈 Trends & Analytics
- Historical analysis and predictive insights
- Performance trends over time
- Growth projections and forecasting
- Advanced statistical analysis

## Data Configuration

### Google Sheets Integration

The dashboard is configured to work with your Google Sheets data:
- **Spreadsheet ID**: `17SFltoaYiEVVHDN7flctrHn1TKj01xCCyrsoiCN7L8c`
- **Expected Sheets**: Dataset, Patient Count, Utilization, Jan-Aug monthly data

### Sample Data Mode

Currently, the dashboard runs with sample data that mimics your actual structure:
- 38 scribes across two teams
- Realistic performance metrics
- Historical trend data
- Provider assignment information

## Customization Options

### Themes and Styling
- Professional, modern UI design
- Responsive layout for different screen sizes
- Custom color schemes for teams
- Interactive charts and visualizations

### Dashboard Configuration
Edit `config/settings.py` to customize:
- Refresh intervals
- Performance thresholds
- Team configurations
- Chart preferences

### Adding New Features
The modular architecture allows easy addition of:
- New dashboard pages
- Additional metrics
- Custom charts
- Enhanced analytics

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`

2. **Port Already in Use**: If port 8501 is busy, Streamlit will automatically use the next available port

3. **Data Loading Issues**: The app will use sample data if Google Sheets connection fails

### Performance Optimization

- Data is cached for 5 minutes to improve performance
- Auto-refresh can be disabled for static analysis
- Large datasets are processed in chunks

## Browser Support

The dashboard works best with:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Mobile Compatibility

The dashboard is responsive and works on:
- Tablets (iPad, Android tablets)
- Mobile phones (limited functionality)
- Desktop computers (full functionality)

## Updates and Maintenance

### Regular Updates
- Data refreshes automatically every 30 seconds
- Manual refresh button available
- Cache management built-in

### Backup and Recovery
- Configuration files are stored in `config/`
- Component files in `src/components/`
- Utility functions in `src/utils/`

## Support and Documentation

### File Structure
```
ScribeDash/
├── README.md
├── requirements.txt
├── config/
│   └── settings.py
├── .github/
│   └── instructions/
└── src/
    ├── main.py
    ├── components/
    │   ├── overview.py
    │   ├── team_performance.py
    │   ├── individual_metrics.py
    │   ├── provider_analysis.py
    │   ├── realtime_activity.py
    │   └── trends_analytics.py
    └── utils/
        ├── google_sheets.py
        ├── data_processor.py
        ├── config.py
        ├── helpers.py
        └── styles.py
```

### Key Features
- **Real-time Updates**: Live data monitoring
- **Interactive Charts**: Plotly-powered visualizations
- **Responsive Design**: Works on all device sizes
- **Professional UI**: Clean, modern interface
- **Comprehensive Analytics**: Deep insights into operations

## Getting Started Checklist

- [ ] Install Python 3.8+
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run application: `streamlit run src/main.py`
- [ ] Open browser to `http://localhost:8501`
- [ ] Explore the dashboard features
- [ ] Customize settings as needed

## Next Steps

1. **Connect Real Data**: Set up actual Google Sheets API integration
2. **Custom Alerts**: Configure alert thresholds for your needs
3. **Reports**: Set up automated reporting schedules
4. **User Training**: Train your team on dashboard features
5. **Feedback**: Gather user feedback for improvements

Your ScribeDash dashboard is now ready to provide real-time insights into your medical scribing operations!
