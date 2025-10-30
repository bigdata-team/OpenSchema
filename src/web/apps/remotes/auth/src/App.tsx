import { Routes, Route } from "react-router";
import Home from './pages/Home';
import About from './pages/About';
import { ProtectedPage } from './components/ProtectedPage';
import { AuthProvider } from './contexts/AuthContext';

// css import is required here for tailwind to work on host
import '@/index.css';

// Export auth components for Module Federation
export { LoginButton } from './components/LoginButton';
export { UserProfile } from './components/UserProfile';
export { AuthWidget } from './layouts/AuthWidget';
export { useAuth, AuthProvider as AuthProviderExport } from './contexts/AuthContext';

function App() {
  return (
    <AuthProvider requireAuth={false}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/protected" element={<ProtectedPage />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
