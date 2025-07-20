# UK Mortgage Calculator

An intelligent mortgage repayment calculator that leverages Bank of England interest rate data and machine learning to provide comprehensive mortgage analysis and interest rate forecasting.

## 🎯 Features

### 💰 Comprehensive Mortgage Calculations
- Calculate monthly repayments based on loan amount, property value, and personal outgoings
- Real-time affordability analysis with debt-to-income ratios
- Loan-to-value (LTV) calculations

### 📈 Overpayment Analysis
- Model one-off and recurring overpayments to understand their impact
- Calculate interest savings and time reduction
- Flexible overpayment frequencies (monthly, annual, one-off)

### 🧠 AI-Powered Interest Rate Forecasting
- Uses Bank of England historical data and machine learning to predict future interest rates
- Provides optimistic, pessimistic, and base-case scenarios
- Random Forest regression with multiple statistical features

### 📊 Smart Data Pipeline
- **Daily CRON job**: Automated Bank of England interest rate data collection
- **Weekly CRON job**: Statistical model retraining and forecast updates
- Real-time API integration with BoE Statistical Database

## 🏗️ Architecture

### Backend (Azure Functions - Python)
- **Mortgage Calculator Engine**: Core calculation logic for repayments and overpayments
- **Data Collection Service**: Automated BoE interest rate data fetching
- **ML Forecasting Service**: Machine learning models for interest rate prediction
- **RESTful API**: Endpoints for frontend integration

### Frontend (React - Azure Static Web App)
- Modern, responsive React application with TypeScript
- Interactive mortgage calculator interface
- Data visualization for interest rate forecasts and scenarios
- Mobile-friendly design with Tailwind CSS

### Infrastructure & Deployment
- **Azure Functions**: Serverless backend with consumption-based pricing
- **Azure Static Web Apps**: Global CDN and seamless CI/CD
- **Bicep Templates**: Infrastructure as Code for reproducible deployments
- **Azure Developer CLI**: One-command deployment with `azd up`

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Azure Functions Core Tools v4
- Azure CLI (for deployment)

### Local Development

1. **Clone and setup:**
   ```bash
   git clone https://github.com/rich-sykes/uk-mortgage-calculator.git
   cd uk-mortgage-calculator
   ./scripts/setup.sh
   ```

2. **Start the backend:**
   ```bash
   cd api
   func start
   ```

3. **Start the frontend (new terminal):**
   ```bash
   cd web
   npm run dev
   ```

4. **Open your browser:**
   - Web app: http://localhost:3000
   - API docs: http://localhost:7071

### Deploy to Azure

```bash
azd auth login
azd up
```

## 🔧 Technology Stack

### Backend
- **Python 3.11** with Azure Functions
- **pandas & scikit-learn** for data processing and ML
- **requests** for Bank of England API integration
- **Azure Managed Identity** for secure authentication

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for responsive design
- **Chart.js** for data visualization
- **Lucide React** for icons

### Infrastructure
- **Azure Functions** (Consumption Plan)
- **Azure Static Web Apps** (Free tier)
- **Azure Storage** for function data
- **Application Insights** for monitoring
- **Bicep** for Infrastructure as Code

## 📊 Data Sources & ML Pipeline

### Bank of England Integration
- **API**: BoE Statistical Database (IUDBEDR series - Bank Rate)
- **Collection**: Daily automated updates at 6 AM UTC
- **Storage**: Azure Storage with versioning
- **Reliability**: Fallback to sample data during API issues

### Machine Learning Features
- Historical rate trends and moving averages (3, 6, 12 months)
- Seasonal and cyclical pattern detection
- Rate change momentum analysis (1m, 3m changes)
- Lag variables (1, 3, 6, 12 month lags)

### Model Details
- **Algorithm**: Random Forest Regression (100 estimators)
- **Training**: Weekly automated retraining on Sundays
- **Validation**: Train/test split with temporal ordering
- **Scenarios**: Base prediction with ±0.25% uncertainty bands

## 🌐 API Reference

### Calculate Mortgage
```http
POST /api/mortgage/calculate
Content-Type: application/json

{
  "loan_amount": 250000,
  "property_value": 300000,
  "annual_rate": 4.5,
  "term_years": 25,
  "monthly_outgoings": 1500,
  "overpayments": {
    "amount": 200,
    "frequency": "monthly"
  }
}
```

### Get Interest Rate Forecasts
```http
GET /api/forecast/predict?months=12&retrain=false
```

### Trigger Data Collection
```http
POST /api/data/collect
```

## 🔍 What Makes This Different

Unlike traditional mortgage calculators, this application:

- **Uses Real Data**: Direct integration with Bank of England official statistics
- **Predicts the Future**: ML-powered interest rate forecasting with multiple scenarios
- **Updates Automatically**: Daily data collection and weekly model retraining
- **Provides Intelligence**: Comprehensive affordability analysis beyond basic calculations
- **Scales Globally**: Serverless architecture with global CDN distribution

## 📈 Performance & Reliability

- **Sub-second** API response times
- **99.9%** uptime with Azure Functions
- **Global** distribution via Azure Static Web Apps CDN
- **Auto-scaling** based on demand
- **Cost-optimized** with consumption-based pricing

## 🛡️ Security & Privacy

- **HTTPS Everywhere**: All communication encrypted
- **Managed Identity**: No stored secrets or connection strings
- **CORS Protection**: Configured for legitimate domains only
- **No Data Storage**: Personal calculations not stored
- **Privacy First**: No tracking or analytics on user data

## 📚 Documentation

- [Development Guide](./docs/DEVELOPMENT.md) - Setup, API docs, and contribution guidelines
- [Architecture Overview](./docs/ARCHITECTURE.md) - Detailed technical architecture
- [Deployment Guide](./docs/DEPLOYMENT.md) - Production deployment instructions

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## ⚖️ Disclaimer

This calculator provides estimates for informational purposes only and should not be considered financial advice. Interest rate predictions are based on historical data and statistical models, and actual rates may vary significantly. Please consult with a qualified mortgage advisor for professional guidance.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bank of England** for providing open access to their statistical data
- **Azure** for the excellent serverless and static hosting platform
- **scikit-learn** community for the machine learning tools
- **React** and **TypeScript** communities for the frontend technologies

---

**Built with ❤️ using Azure, Python, React, and real Bank of England data**
