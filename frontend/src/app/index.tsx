import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@shared/lib/i18n";
import "@shared/styles/index.css";
import { App } from "./App";

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Root element not found");
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
