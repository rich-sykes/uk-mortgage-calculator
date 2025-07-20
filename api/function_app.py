import azure.functions as func
import logging
import json
from datetime import datetime, timezone
from shared_code import calculator, data_collector, predictor

# Initialize the Function App
app = func.FunctionApp()


@app.route(
    route="mortgage/calculate", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"]
)
def mortgage_calculator(req: func.HttpRequest) -> func.HttpResponse:
    """
    Calculate mortgage repayments with optional overpayment scenarios.
    """
    logging.info("Processing mortgage calculation request.")

    try:
        # Parse request body
        req_body = req.get_json()
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "Request body is required"}),
                status_code=400,
                mimetype="application/json",
            )

        # Validate required fields
        required_fields = ["loan_amount", "property_value", "annual_rate", "term_years"]
        missing_fields = [field for field in required_fields if field not in req_body]

        if missing_fields:
            return func.HttpResponse(
                json.dumps(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"}
                ),
                status_code=400,
                mimetype="application/json",
            )

        # Extract parameters
        loan_amount = float(req_body["loan_amount"])
        property_value = float(req_body["property_value"])
        annual_rate = (
            float(req_body["annual_rate"]) / 100
        )  # Convert percentage to decimal
        term_years = int(req_body["term_years"])
        monthly_outgoings = float(req_body.get("monthly_outgoings", 0))

        # Calculate basic mortgage details
        monthly_payment = calculator.calculate_monthly_payment(
            loan_amount, annual_rate, term_years
        )
        total_payment = monthly_payment * term_years * 12
        total_interest = total_payment - loan_amount

        # Calculate LTV ratio
        ltv_ratio = (loan_amount / property_value) * 100

        # Calculate required monthly income (rough estimate: payment should be max 30% of income)
        monthly_income_required = (monthly_payment + monthly_outgoings) / 0.3

        # Build response
        response_data = {
            "loan_amount": loan_amount,
            "property_value": property_value,
            "annual_rate": annual_rate * 100,  # Convert back to percentage
            "term_years": term_years,
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2),
            "ltv_ratio": round(ltv_ratio, 2),
            "monthly_income_required": round(monthly_income_required, 2),
            "monthly_outgoings": monthly_outgoings,
        }

        # Handle overpayment scenarios if provided
        if "overpayments" in req_body:
            overpayment_data = req_body["overpayments"]
            overpayment_amount = float(overpayment_data.get("amount", 0))
            frequency = overpayment_data.get("frequency", "monthly")

            if overpayment_amount > 0:
                overpayment_analysis = calculator.calculate_overpayment_impact(
                    loan_amount, annual_rate, term_years, overpayment_amount, frequency
                )
                response_data["overpayment_analysis"] = overpayment_analysis

        return func.HttpResponse(
            json.dumps(response_data), status_code=200, mimetype="application/json"
        )

    except ValueError as e:
        logging.error(f"Validation error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Invalid input: {str(e)}"}),
            status_code=400,
            mimetype="application/json",
        )
    except Exception as e:
        logging.error(f"Unexpected error in mortgage calculation: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json",
        )


@app.route(
    route="data/collect", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST", "GET"]
)
def data_collection_function(req: func.HttpRequest = None) -> func.HttpResponse:
    """
    Collect Bank of England interest rate data.
    Can be triggered via HTTP or timer.
    """
    utc_timestamp = datetime.now(timezone.utc).isoformat()

    # Determine trigger type
    trigger_type = "http"

    try:
        # Collect data
        data_result = data_collector.fetch_interest_rates()

        response_data = {
            "timestamp": utc_timestamp,
            "trigger_type": trigger_type,
            "status": "success",
            "data_collected": len(data_result)
            if hasattr(data_result, "__len__")
            else 0,
        }

        logging.info(f"Data collection completed: {len(data_result)} records")

        # Return HTTP response only for HTTP triggers
        if trigger_type == "http":
            return func.HttpResponse(
                json.dumps(response_data), status_code=200, mimetype="application/json"
            )

    except Exception as e:
        error_msg = f"Error in data collection: {str(e)}"
        logging.error(error_msg)

        if trigger_type == "http":
            return func.HttpResponse(
                json.dumps(
                    {
                        "timestamp": utc_timestamp,
                        "trigger_type": trigger_type,
                        "status": "error",
                        "error": str(e),
                    }
                ),
                status_code=500,
                mimetype="application/json",
            )


@app.route(
    route="forecast/predict", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"]
)
def ml_forecasting_function(req: func.HttpRequest = None) -> func.HttpResponse:
    """
    Generate ML-based interest rate forecasts.
    Can be triggered via HTTP or timer (weekly retraining).
    """
    utc_timestamp = datetime.now(timezone.utc).isoformat()

    # Determine trigger type
    logging.info(f"ML forecaster HTTP trigger executed at: {utc_timestamp}")
    trigger_type = "http"
    # Check if retrain is requested via query parameter
    force_retrain = (
        req.params.get("retrain", "false").lower() == "true" if req else False
    )

    try:
        # Get forecast parameters
        months_ahead = int(req.params.get("months", 12)) if req else 12

        # Get recent data for prediction
        recent_data = data_collector.fetch_interest_rates()

        # Generate forecasts
        if force_retrain and len(recent_data) > 0:
            logging.info("Retraining ML model...")
            predictor.train_model(recent_data)

        forecasts = predictor.predict_rates(recent_data, months_ahead=months_ahead)

        response_data = {
            "timestamp": utc_timestamp,
            "trigger_type": trigger_type,
            "status": "success",
            "model_retrained": force_retrain,
            "months_ahead": months_ahead,
            "forecasts": forecasts,
        }

        logging.info(f"ML forecasting completed: {months_ahead} predictions")

        # Return HTTP response only for HTTP triggers
        if trigger_type == "http":
            return func.HttpResponse(
                json.dumps(response_data), status_code=200, mimetype="application/json"
            )

    except Exception as e:
        error_msg = f"Error in ML forecasting: {str(e)}"
        logging.error(error_msg)

        if trigger_type == "http":
            return func.HttpResponse(
                json.dumps(
                    {
                        "timestamp": utc_timestamp,
                        "trigger_type": trigger_type,
                        "status": "error",
                        "error": str(e),
                    }
                ),
                status_code=500,
                mimetype="application/json",
            )


@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Simple health check endpoint.
    """
    return func.HttpResponse(
        json.dumps(
            {
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": "2.0",
            }
        ),
        status_code=200,
        mimetype="application/json",
    )
