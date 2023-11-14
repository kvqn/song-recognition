import React from "react"
import { useNavigate } from "react-router-dom"

const NavBar = () => {
  const navigate = useNavigate()
  const linkStyle =
    "px-4 py-2 text-base font-semibold text-gray-700 hover:text-blue-500 cursor-pointer transition duration-300 ease-in-out transform hover:scale-105"
  const activeLinkStyle = "border-b-4 border-blue-500"

  const getLinkStyle = (path) => {
    return window.location.pathname === path
      ? `${linkStyle} ${activeLinkStyle}`
      : linkStyle
  }

  return (
    <nav className="sticky top-0 bg-white pt-2 shadow-md">
      <div className="flex justify-center space-x-4">
        <div className={getLinkStyle("/app")} onClick={() => navigate("/app")}>
          App
        </div>
        <div
          className={getLinkStyle("/archive")}
          onClick={() => navigate("/archive")}
        >
          Song Archive
        </div>
        <div
          className={getLinkStyle("/about")}
          onClick={() => navigate("/about")}
        >
          About Model
        </div>
      </div>
    </nav>
  )
}

export default NavBar
