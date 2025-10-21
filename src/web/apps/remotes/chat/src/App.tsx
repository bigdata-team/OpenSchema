import { Routes, Route } from "react-router";
import Home from './pages/Home';
import About from './pages/About';
import ChatTest from './pages/ChatTest';

// css import is required here for tailwind to work on host
// import './index.css';
import "@/index.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/chat" element={<ChatTest />} />
    </Routes>
  );
}

export default App;
