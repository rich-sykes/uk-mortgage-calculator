export function About() {
    return (
        <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    About UK Mortgage Calculator
                </h1>
                <p className="text-lg text-gray-600">
                    The most advanced mortgage calculator with AI-powered interest rate forecasting
                </p>
            </div>

            <div className="space-y-8">
                <div className="card">
                    <h2 className="text-2xl font-semibold mb-4">What Makes Us Different</h2>
                    <div className="space-y-4 text-gray-700">
                        <p>
                            Unlike traditional mortgage calculators, we leverage real Bank of England
                            interest rate data combined with machine learning algorithms to provide
                            you with intelligent forecasting capabilities.
                        </p>
                        <ul className="list-disc list-inside space-y-2">
                            <li>Real-time Bank of England interest rate data integration</li>
                            <li>Machine learning models for interest rate prediction</li>
                            <li>Optimistic and pessimistic scenario modeling</li>
                            <li>Comprehensive overpayment impact analysis</li>
                            <li>Daily data updates and weekly model retraining</li>
                        </ul>
                    </div>
                </div>

                <div className="card">
                    <h2 className="text-2xl font-semibold mb-4">Technology Stack</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h3 className="font-semibold mb-2">Backend (Azure Functions)</h3>
                            <ul className="text-gray-700 space-y-1">
                                <li>• Python with pandas and scikit-learn</li>
                                <li>• Bank of England API integration</li>
                                <li>• Random Forest regression models</li>
                                <li>• Automated CRON scheduling</li>
                            </ul>
                        </div>
                        <div>
                            <h3 className="font-semibold mb-2">Frontend (React)</h3>
                            <ul className="text-gray-700 space-y-1">
                                <li>• Modern React with TypeScript</li>
                                <li>• Responsive Tailwind CSS design</li>
                                <li>• Interactive data visualizations</li>
                                <li>• Azure Static Web Apps hosting</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <h2 className="text-2xl font-semibold mb-4">Data Sources & Models</h2>
                    <div className="text-gray-700 space-y-4">
                        <p>
                            Our forecasting models are trained on historical Bank of England base rate
                            data, incorporating various statistical features including:
                        </p>
                        <ul className="list-disc list-inside space-y-1">
                            <li>Historical rate trends and moving averages</li>
                            <li>Seasonal and cyclical patterns</li>
                            <li>Economic indicator correlations</li>
                            <li>Rate change momentum analysis</li>
                        </ul>
                        <p className="text-sm text-gray-500 mt-4">
                            Disclaimer: Predictions are for informational purposes only and should not
                            be considered financial advice. Please consult with a qualified mortgage
                            advisor for professional guidance.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
