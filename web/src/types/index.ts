// Mortgage calculation types
export interface MortgageInputs {
    loanAmount: number;
    propertyValue: number;
    annualRate: number;
    termYears: number;
    monthlyOutgoings: number;
}

export interface OverpaymentInputs {
    amount: number;
    frequency: 'monthly' | 'annual' | 'one_off';
}

export interface MortgageResult {
    loanDetails: {
        loanAmount: number;
        propertyValue: number;
        annualRate: number;
        termYears: number;
        ltvRatio: number;
    };
    paymentDetails: {
        monthlyPayment: number;
        annualPayment: number;
        totalAmountPayable: number;
        totalInterest: number;
    };
    affordability: {
        monthlyOutgoings: number;
        remainingMonthlyIncome: number;
        estimatedDebtToIncome: number;
    };
    overpaymentAnalysis?: {
        newMonthlyPayment: number;
        monthsSaved: number;
        interestSaved: number;
        totalPayments: number;
        yearsSaved: number;
    };
}

// Interest rate forecasting types
export interface InterestRatePrediction {
    baseScenario: number[];
    optimisticScenario: number[];
    pessimisticScenario: number[];
}

export interface ForecastResult {
    status: string;
    modelInfo: {
        isTrained: boolean;
        trainingMetrics: {
            trainR2?: number;
            testR2?: number;
            samplesUsed?: number;
        };
        dataPointsUsed: number;
    };
    predictions: {
        monthsAhead: number;
        scenarios: InterestRatePrediction;
        currentRate: number | null;
    };
    generatedAt: string;
}

// API response types
export interface ApiResponse<T> {
    data?: T;
    error?: string;
    status: number;
}

// Chart data types
export interface ChartDataPoint {
    x: string | number;
    y: number;
}

export interface ChartDataset {
    label: string;
    data: ChartDataPoint[];
    borderColor: string;
    backgroundColor: string;
    fill?: boolean;
}
