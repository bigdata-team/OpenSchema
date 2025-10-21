import { Routes, Route } from "react-router";
import Home from './pages/Home';
import About from './pages/About';
import './index.css'

import React from 'react';

const AuthApp = React.lazy(() => import('auth/App'));
const ChatApp = React.lazy(() => import('chat/App'));

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/auth/*" element={
        <React.Suspense fallback={<div>Loading Remote App...</div>}>
          <AuthApp />
        </React.Suspense>
      } />
      <Route path="/chat/*" element={
        <React.Suspense fallback={<div>Loading Remote App...</div>}>
          <ChatApp />
        </React.Suspense>
      } />
    </Routes>
  );
}

export default App;
