import { Routes, Route } from "react-router";
import Home from './pages/Home';
import About from './pages/About';
import ChatMultiTest from './components/ChatMultiTest';
import Layout from './pages/layout/layout';

// css import is required here for tailwind to work on host
// import './index.css';
import "@/index.css";

function App() {
  return (
    <Routes>
      {/* <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/chat" element={<ChatMultiTest />} /> */}
      <Route path="/" element={<Layout />} >
        <Route path="home" element={<Home />} />
        <Route path="chat" element={<ChatMultiTest />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  );
}

export default App;
