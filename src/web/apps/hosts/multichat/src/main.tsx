import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from "react-router";
import './index.css'
import App from './App.tsx'

const SERVICE_TYPE = import.meta.env.VITE_SERVICE_TYPE ?? 'ui';
const SERVICE_VERSION = import.meta.env.VITE_SERVICE_VERSION ?? 'v1';
const SERVICE_NAME = import.meta.env.VITE_SERVICE_NAME ?? 'host';

const BASE_PATH = `/${SERVICE_TYPE}/${SERVICE_VERSION}/${SERVICE_NAME}`;

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter basename={BASE_PATH}>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
