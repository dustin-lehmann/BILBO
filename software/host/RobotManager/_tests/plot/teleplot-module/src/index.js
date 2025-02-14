import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css"; // global styles

const container = document.getElementById("root");
if (!container) {
  throw new Error("No element with id 'root' found in index.html");
}

const root = createRoot(container);
root.render(<App />);
