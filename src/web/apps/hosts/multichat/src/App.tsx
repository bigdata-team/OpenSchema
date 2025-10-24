import React from 'react';
import { Routes, Route } from "react-router";
// import Home from './pages/Home';
import About from './pages/About';
import '@//index.css'
import Multichat from './pages/Multichat';

const AuthApp = React.lazy(() => import('auth/App'));

function App() {
  return (
    <Routes>
      {/* <Route path="/" element={<Home />} /> */}
      <Route path="/" element={<Multichat /> } />
      <Route path="/about" element={<About />} />
      <Route path="/auth/*" element={
        <React.Suspense fallback={<div>Loading Remote App...</div>}>
          <AuthApp />
        </React.Suspense>
      } /> 
      {/* <Route path="/chat/*" element={<Multichat /> } /> */}
    </Routes>
  );
}

export default App;
