import React from "react"
import { BrowserRouter as Router } from "react-router-dom"

import Routes from "./Routes" // Assuming you have a separate Routes component
import NavBar from "./NavBar"

function App() {
  return (
    <Router>
      <NavBar />
      <Routes />
    </Router>
  )
}

export default App
