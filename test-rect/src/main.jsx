import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { effects as blocksEffects } from "@blocksuite/blocks/effects";
import { effects as presetsEffects } from "@blocksuite/presets/effects";
blocksEffects();
presetsEffects();

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
