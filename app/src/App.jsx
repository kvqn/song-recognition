import { useState } from "react"
import reactLogo from "./assets/react.svg"
import viteLogo from "/vite.svg"
import "./App.css"
import AudioPlay from "./Audioplay"
import UploadPage from "./UploadPage"

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className=" flex items-center justify-center pt-40">
        <div>
          {/* <AudioPlay /> */}
          <UploadPage />
        </div>
      </div>
    </>
  )
}

export default App
