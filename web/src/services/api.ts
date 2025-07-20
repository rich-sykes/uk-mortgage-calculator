import { MortgageInputs, OverpaymentInputs, MortgageResult, ForecastResult, ApiResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

class ApiService {
    private async request<T>(endpoint: string, options?: RequestInit): Promise<ApiResponse<T>> {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options?.headers,
                },
                ...options,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { data, status: response.status };
        } catch (error) {
            console.error('API request failed:', error);
            return {
                error: error instanceof Error ? error.message : 'Unknown error',
                status: 500,
            };
        }
    }

    async calculateMortgage(
        inputs: MortgageInputs,
        overpayments?: OverpaymentInputs
    ): Promise<ApiResponse<MortgageResult>> {
        const payload = {
            loan_amount: inputs.loanAmount,
            property_value: inputs.propertyValue,
            annual_rate: inputs.annualRate,
            term_years: inputs.termYears,
            monthly_outgoings: inputs.monthlyOutgoings,
            ...(overpayments && {
                overpayments: {
                    amount: overpayments.amount,
                    frequency: overpayments.frequency,
                },
            }),
        };

        return this.request<MortgageResult>('/mortgage/calculate', {
            method: 'POST',
            body: JSON.stringify(payload),
        });
    }

    async getInterestRateForecasts(
        monthsAhead: number = 12,
        retrain: boolean = false
    ): Promise<ApiResponse<ForecastResult>> {
        const params = new URLSearchParams({
            months: monthsAhead.toString(),
            retrain: retrain.toString(),
        });

        return this.request<ForecastResult>(`/forecast/predict?${params}`);
    }

    async triggerDataCollection(): Promise<ApiResponse<{ status: string; recordsFetched: number }>> {
        return this.request('/data/collect', {
            method: 'POST',
        });
    }
}

export const apiService = new ApiService();
