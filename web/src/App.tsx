import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { Navigation } from './components/Navigation';
import { MortgageCalculator } from './pages/MortgageCalculator';
import { InterestRateForecasts } from './pages/InterestRateForecasts';
import { About } from './pages/About';

function App() {
    return (
        <ThemeProvider>
            <Router>
                <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
                    <Navigation />
                    <main className="container mx-auto px-4 py-8">
                        <Routes>
                            <Route path="/" element={<MortgageCalculator />} />
                            <Route path="/forecasts" element={<InterestRateForecasts />} />
                            <Route path="/about" element={<About />} />
                        </Routes>
                    </main>
                </div>
            </Router>
        </ThemeProvider>
    );
}

export default App;
