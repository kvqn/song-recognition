import React from "react"
import ReactDOM from "react-dom/client"
import App from "./App"
import "./index.css"
import ErrorBoundary from "./ErrorBoundary"
import { Route, Router, Routes } from "react-router-dom"

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
)
