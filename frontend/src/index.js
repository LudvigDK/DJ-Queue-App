import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import GuestPage from './components/GuestPage';
import EventDashboard from './components/EventDashboard';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<App />} />
      <Route path='/dashboard' element={<EventDashboard />} />
      <Route path='/guest/:code' element={<GuestPage />} />
    </Routes>
  </BrowserRouter>
);
