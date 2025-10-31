// import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from "react-router";
import App from './App'

import '@/index.css'

const BASE_PATH = `/ui/v1/chat`;

createRoot(document.getElementById('root')!).render(
  // <StrictMode>
    <BrowserRouter basename={BASE_PATH}>
      <App />
    </BrowserRouter>
  // </StrictMode>,
)
