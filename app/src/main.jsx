import React from "react"
import ReactDOM from "react-dom/client"
import App from "./App"
import "./index.css"
import ErrorBoundary from "./ErrorBoundary"
import { Route, Router, Routes } from "react-router-dom"
import Navbar from "./NavBar"
import UploadPage from "./UploadPage"

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
)
