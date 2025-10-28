// import React from 'react';
import { Routes, Route } from "react-router";
import Home from './pages/Home';
import About from './pages/About';
import '@/index.css'
import ChatMultiTest from './pages/ChatMultiTest';
import Layout from './pages/layout/layout';

// const AuthApp = React.lazy(() => import('auth/App'));

function App() {
  return (
    <Routes>
      {/* <Route path="/" element={<Home />} /> */}
      {/* <Route path="/" element={<Multichat /> } />
      <Route path="/about" element={<About />} />
      <Route path="/auth/*" element={
        <React.Suspense fallback={<div>Loading Remote App...</div>}>
          <AuthApp />
        </React.Suspense>
      } />  */}
      {/* <Route path="/chat/*" element={<Multichat /> } /> */}

      <Route path="/" element={<Layout />} >
        <Route path="home" element={<Home />} />
        <Route path="chat" element={<ChatMultiTest />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  );
}

export default App;
