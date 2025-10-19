import { Routes, Route } from "react-router";
import Home from './pages/Home';
import About from './pages/About';
import './index.css'

import React from 'react';

// const RemoteApp = React.lazy(() => import('remote/App'));
const RemoteApp = React.lazy(() => import('chat/App'));


function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/remote/*" element={
        <React.Suspense fallback={<div>Loading Remote App...</div>}>
          <RemoteApp />
        </React.Suspense>
      } />
    </Routes>
  );
}

export default App;
