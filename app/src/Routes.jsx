import React from "react"
import { Route, Routes } from "react-router-dom"
import UploadPage from "./UploadPage"
import SongArchive from "./SongArchive"
import AboutModel from "./AboutModel"

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/app" element={<UploadPage />} />
      <Route path="/archive" element={<SongArchive />} />
      <Route path="/about" element={<AboutModel />} />
      <Route path="/" element={<UploadPage />} />
    </Routes>
  )
}

export default AppRoutes
