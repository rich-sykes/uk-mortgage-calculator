import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { MortgageInputs, OverpaymentInputs, MortgageResult } from '../types';
import { Calculator, PoundSterling, TrendingDown, TrendingUp } from 'lucide-react';

export function MortgageCalculator() {
    const [inputs, setInputs] = useState<MortgageInputs>({
        loanAmount: 250000,
        propertyValue: 300000,
        annualRate: 4.5,
        termYears: 25,
        monthlyOutgoings: 1500,
    });

    const [overpayments, setOverpayments] = useState<OverpaymentInputs>({
        amount: 0,
        frequency: 'monthly',
    });

    const [result, setResult] = useState<MortgageResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const calculateMortgage = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await apiService.calculateMortgage(
                inputs,
                overpayments.amount > 0 ? overpayments : undefined
            );

            if (response.error) {
                setError(response.error);
            } else if (response.data) {
                setResult(response.data);
            }
        } catch (err) {
            setError('Failed to calculate mortgage');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        calculateMortgage();
    }, []);

    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat('en-GB', {
            style: 'currency',
            currency: 'GBP',
        }).format(amount);
    };

    const formatPercentage = (value: number) => {
        return `${value.toFixed(2)}%`;
    };

    return (
        <div className="max-w-6xl mx-auto space-y-8">
            <div className="text-center">
                <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                    UK Mortgage Calculator
                </h1>
                <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
                    Calculate your mortgage payments with intelligent interest rate forecasting
                    powered by Bank of England data and machine learning.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Input Form */}
                <div className="card">
                    <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6 flex items-center">
                        <Calculator className="h-6 w-6 mr-2 text-blue-600 dark:text-blue-400" />
                        Mortgage Details
                    </h2>

                    <div className="space-y-4">
                        <div>
                            <label className="label mb-1">
                                Loan Amount
                            </label>
                            <input
                                type="number"
                                className="input"
                                value={inputs.loanAmount}
                                onChange={(e) => setInputs({ ...inputs, loanAmount: Number(e.target.value) })}
                            />
                        </div>

                        <div>
                            <label className="label mb-1">
                                Property Value
                            </label>
                            <input
                                type="number"
                                className="input"
                                value={inputs.propertyValue}
                                onChange={(e) => setInputs({ ...inputs, propertyValue: Number(e.target.value) })}
                            />
                        </div>

                        <div>
                            <label className="label mb-1">
                                Annual Interest Rate (%)
                            </label>
                            <input
                                type="number"
                                step="0.01"
                                className="input"
                                value={inputs.annualRate}
                                onChange={(e) => setInputs({ ...inputs, annualRate: Number(e.target.value) })}
                            />
                        </div>

                        <div>
                            <label className="label mb-1">
                                Term (Years)
                            </label>
                            <input
                                type="number"
                                className="input"
                                value={inputs.termYears}
                                onChange={(e) => setInputs({ ...inputs, termYears: Number(e.target.value) })}
                            />
                        </div>

                        <div>
                            <label className="label mb-1">
                                Monthly Outgoings
                            </label>
                            <input
                                type="number"
                                className="input"
                                value={inputs.monthlyOutgoings}
                                onChange={(e) => setInputs({ ...inputs, monthlyOutgoings: Number(e.target.value) })}
                            />
                        </div>
                    </div>

                    <div className="mt-8">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            Overpayments (Optional)
                        </h3>

                        <div className="space-y-4">
                            <div>
                                <label className="label mb-1">
                                    Overpayment Amount
                                </label>
                                <input
                                    type="number"
                                    className="input"
                                    value={overpayments.amount}
                                    onChange={(e) => setOverpayments({ ...overpayments, amount: Number(e.target.value) })}
                                />
                            </div>

                            <div>
                                <label className="label mb-1">
                                    Frequency
                                </label>
                                <select
                                    className="input"
                                    value={overpayments.frequency}
                                    onChange={(e) => setOverpayments({ ...overpayments, frequency: e.target.value as any })}
                                >
                                    <option value="monthly">Monthly</option>
                                    <option value="annual">Annual</option>
                                    <option value="one_off">One-off</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <button
                        onClick={calculateMortgage}
                        disabled={loading}
                        className="btn btn-primary w-full mt-6"
                    >
                        {loading ? 'Calculating...' : 'Calculate Mortgage'}
                    </button>

                    {error && (
                        <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300">
                            {error}
                        </div>
                    )}
                </div>

                {/* Results */}
                <div className="space-y-6">
                    {result && (
                        <>
                            {/* Payment Summary */}
                            <div className="card">
                                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                                    <PoundSterling className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
                                    Payment Summary
                                </h3>

                                <div className="space-y-3">
                                    <div className="flex justify-between">
                                        <span className="text-gray-600 dark:text-gray-300">Monthly Payment:</span>
                                        <span className="font-semibold text-lg text-gray-900 dark:text-white">
                                            {formatCurrency(result.paymentDetails.monthlyPayment)}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600 dark:text-gray-300">Total Interest:</span>
                                        <span className="font-medium text-gray-900 dark:text-white">
                                            {formatCurrency(result.paymentDetails.totalInterest)}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600 dark:text-gray-300">Total Amount Payable:</span>
                                        <span className="font-medium text-gray-900 dark:text-white">
                                            {formatCurrency(result.paymentDetails.totalAmountPayable)}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Loan-to-Value (LTV):</span>
                                        <span className="font-medium">
                                            {formatPercentage(result.loanDetails.ltvRatio)}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            {/* Overpayment Analysis */}
                            {result.overpaymentAnalysis && (
                                <div className="card">
                                    <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                                        <TrendingUp className="h-5 w-5 mr-2 text-blue-600" />
                                        Overpayment Impact
                                    </h3>

                                    <div className="space-y-3">
                                        <div className="flex justify-between">
                                            <span className="text-gray-600">Interest Saved:</span>
                                            <span className="font-semibold text-green-600">
                                                {formatCurrency(result.overpaymentAnalysis.interestSaved)}
                                            </span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-gray-600">Time Saved:</span>
                                            <span className="font-medium">
                                                {result.overpaymentAnalysis.yearsSaved} years
                                            </span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-gray-600">New Monthly Payment:</span>
                                            <span className="font-medium">
                                                {formatCurrency(result.overpaymentAnalysis.newMonthlyPayment)}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Affordability */}
                            <div className="card">
                                <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                                    <TrendingDown className="h-5 w-5 mr-2 text-orange-600" />
                                    Affordability
                                </h3>

                                <div className="space-y-3">
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Monthly Outgoings:</span>
                                        <span className="font-medium">
                                            {formatCurrency(result.affordability.monthlyOutgoings)}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Remaining Income:</span>
                                        <span className="font-medium">
                                            {formatCurrency(result.affordability.remainingMonthlyIncome)}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Debt-to-Income Ratio:</span>
                                        <span className="font-medium">
                                            {formatPercentage(result.affordability.estimatedDebtToIncome)}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}
