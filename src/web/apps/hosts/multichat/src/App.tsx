import { Routes, Route } from "react-router";
import Home from './pages/Home';
import About from './pages/About';
import '@/index.css'
import Layout from "@/pages/layout/Layout";

import ChatMultiTest from '@/pages/ChatMultiTest';

// import React from 'react';
// const AuthApp = React.lazy(() => import('auth/App'));
// const ChatMultiTest = React.lazy(() => import('chat/ChatMultiTest'));
// const Layout = React.lazy(() => import('chat/Layout'));

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
