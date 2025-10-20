import { Routes, Route } from "react-router";
import Home from './pages/Home';
import About from './pages/About';

// css import is required here for tailwind to work on host
import '@/index.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
    </Routes>
  );
}

export default App;
