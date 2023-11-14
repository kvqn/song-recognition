import React from "react"
import { BrowserRouter as Router } from "react-router-dom"

import Routes from "./Routes" // Assuming you have a separate Routes component
import Navbar from "./NavBar"

function App() {
  return (
    <Router>
      <Navbar />
      <Routes />
    </Router>
  )
}

export default App
