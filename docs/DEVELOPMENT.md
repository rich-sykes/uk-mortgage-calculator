# UK Mortgage Calculator Development Guide

## Overview

This project consists of:
- **Backend**: Python Azure Functions for mortgage calculations, data collection, and ML forecasting
- **Frontend**: React TypeScript application hosted on Azure Static Web Apps
- **Infrastructure**: Bicep templates for Azure deployment

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- Azure Functions Core Tools v4
- Azure CLI (for deployment)

### Quick Start

1. **Run the setup script:**
   ```bash
   ./scripts/setup.sh
   ```

2. **Start the API server:**
   ```bash
   cd api
   func start
   ```

3. **Start the web development server (new terminal):**
   ```bash
   cd web
   npm run dev
   ```

4. **Open your browser:**
   - Web app: http://localhost:3000
   - API: http://localhost:7071

## Architecture

### Backend Functions

- **`mortgage_calculator`**: HTTP trigger for mortgage calculations
- **`data_collector`**: Timer trigger (daily) + HTTP trigger for BoE data collection
- **`ml_forecaster`**: Timer trigger (weekly) + HTTP trigger for ML predictions

### Frontend Pages

- **Calculator**: Main mortgage calculation interface
- **Forecasts**: Interest rate prediction visualizations
- **About**: Project information and technology details

## API Endpoints

### Mortgage Calculator
```
POST /api/mortgage/calculate
```

Request body:
```json
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

### Interest Rate Forecasts
```
GET /api/forecast/predict?months=12&retrain=false
```

### Data Collection
```
POST /api/data/collect
```

## Deployment

### Using Azure Developer CLI (azd)

1. **Initialize environment:**
   ```bash
   azd auth login
   azd init
   ```

2. **Deploy to Azure:**
   ```bash
   azd up
   ```

### Manual Deployment

1. **Deploy infrastructure:**
   ```bash
   az deployment group create \
     --resource-group <your-rg> \
     --template-file infra/main.bicep \
     --parameters infra/main.parameters.json
   ```

2. **Deploy Functions:**
   ```bash
   cd api
   func azure functionapp publish <function-app-name>
   ```

3. **Deploy Static Web App:**
   ```bash
   cd web
   npm run build
   # Deploy dist/ folder to Static Web App
   ```

## Environment Variables

### Required for Functions
- `AZURE_CLIENT_ID`: Managed identity client ID
- `APPLICATIONINSIGHTS_CONNECTION_STRING`: Application Insights connection string

### Optional
- `BOE_API_BASE_URL`: Bank of England API base URL (defaults to official API)
- `STORAGE_CONNECTION_STRING`: Azure Storage connection string

## Bank of England API

The application uses the Bank of England's Statistical API to fetch historical interest rate data:
- **Endpoint**: https://www.bankofengland.co.uk/boeapps/database
- **Series**: IUDBEDR (Bank Rate)
- **Format**: JSON

## Machine Learning Model

The forecasting system uses:
- **Algorithm**: Random Forest Regression
- **Features**: Historical rates, moving averages, lag variables, seasonal patterns
- **Training**: Weekly automated retraining
- **Scenarios**: Base, optimistic, and pessimistic predictions

## Development Commands

### API Development
```bash
cd api

# Install dependencies
pip install -r requirements.txt

# Start local Functions host
func start

# Run specific function
func start --functions mortgage_calculator
```

### Web Development
```bash
cd web

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint
```

## Testing

### API Testing
```bash
cd api

# Test mortgage calculation
curl -X POST http://localhost:7071/api/mortgage/calculate \
  -H "Content-Type: application/json" \
  -d '{"loan_amount": 250000, "annual_rate": 4.5, "term_years": 25}'

# Test data collection
curl -X POST http://localhost:7071/api/data/collect

# Test forecasting
curl http://localhost:7071/api/forecast/predict?months=12
```

### Frontend Testing
The React app includes a test suite using Vitest:
```bash
cd web
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## Security

- All API endpoints use HTTPS
- Managed Identity for Azure service authentication
- No hardcoded secrets or API keys
- CORS configured for frontend domain

## License

This project is licensed under the MIT License - see the LICENSE file for details.
