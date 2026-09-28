import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { Dashboard } from './pages/Dashboard';
import { NewReview } from './pages/NewReview';
import { ReportDetail } from './pages/ReportDetail';
import { ReportHistory } from './pages/ReportHistory';
import { SettingsAbout } from './pages/SettingsAbout';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
        <Header />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/new-review" element={<NewReview />} />
            <Route path="/reports/:id" element={<ReportDetail />} />
            <Route path="/history" element={<ReportHistory />} />
            <Route path="/settings" element={<SettingsAbout />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
};

export default App;
