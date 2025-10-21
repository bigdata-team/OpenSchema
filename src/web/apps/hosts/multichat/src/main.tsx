import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from "react-router";
import App from './App'

import '@/index.css'

//const BASE_PATH = `/ui/v1/multichat`;

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {/* <BrowserRouter basename={BASE_PATH}> */}
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
