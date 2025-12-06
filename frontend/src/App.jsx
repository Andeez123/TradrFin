import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import MainLayout from './layout/MainLayout';
import Dashboard from './pages/Dashboard';
import Verification from './pages/Verification';
import Advisor from './pages/Advisor';
import BankingDashboard from './pages/BankingDashboard';
import AIInvest from './pages/AIInvest';
import Transfer from './pages/Transfer';
import Sentiment from './pages/Sentiment';
import Technicals from './pages/Technicals';
import History from './pages/History';

// Component to force re-mounting on navigation
function AppRoutes() {
  const location = useLocation();

  // Scroll to top on navigation
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);

  return (
    <Routes location={location} key={location.pathname}>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<BankingDashboard key={location.pathname} />} />
        <Route path="transfers" element={<Transfer key={location.pathname} />} />
        <Route path="history" element={<History key={location.pathname} />} />
        <Route path="ai-invest" element={<AIInvest key={location.pathname} />} />
        <Route path="sentiment" element={<Sentiment key={location.pathname} />} />
        <Route path="technicals" element={<Technicals key={location.pathname} />} />
        <Route path="verification" element={<Verification key={location.pathname} />} />
        <Route path="advisor" element={<Advisor key={location.pathname} />} />
              </Route>
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}

export default App;