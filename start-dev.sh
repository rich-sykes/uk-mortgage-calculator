#!/bin/bash

echo "Starting UK Mortgage Calculator Frontend and Backend..."

# Start the frontend in the background
echo "Starting React frontend..."
cd /Users/richardsykes/dev/uk-mortgage-calculator/web && npx vite &
FRONTEND_PID=$!

# Start the backend
echo "Starting Azure Functions backend..."
cd /Users/richardsykes/dev/uk-mortgage-calculator/api && func start &
BACKEND_PID=$!

echo "Frontend PID: $FRONTEND_PID"
echo "Backend PID: $BACKEND_PID"
echo ""
echo "Frontend running at: http://localhost:5173"
echo "Backend running at: http://localhost:7071"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for interrupt
wait
