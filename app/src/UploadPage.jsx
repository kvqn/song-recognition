import { useState } from "react"
import axios from "axios"

const UploadPage = () => {
  const [audioFile, setAudioFile] = useState(null)
  const [text, setText] = useState("")
  const [response, setResponse] = useState(null)
  const [loadingMessage, setLoadingMessage] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)

  const loadingMessages = [
    "Uploading audio...",
    "Analyzing the uploaded audio...",
    "Analyzing and parsing text...",
    "Requesting server...",
    "Getting response...",
    "Hang in for a moment...",
  ]

  const handleAudioChange = (event) => {
    setAudioFile(event.target.files[0])
  }

  const handleTextChange = (event) => {
    setText(event.target.value)
  }

  const cycleLoadingMessages = (index = 0) => {
    setLoadingMessage(loadingMessages[index])
    index = (index + 1) % loadingMessages.length

    const timer = setTimeout(() => cycleLoadingMessages(index), 1000)
    return () => clearTimeout(timer)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!audioFile && !text) {
      setError("Please upload an audio file or enter text")
      return
    }

    setError(null)

    setIsSubmitting(true)
    cycleLoadingMessages()

    const formData = new FormData()
    console.log(audioFile)
    if (audioFile) formData.append("audio", audioFile)
    if (text) formData.append("text", text)

    let url
    if (audioFile && text)
      url = "http://100.101.242.147:8000/predict/audio-and-text"
    if (audioFile && !text) url = "http://100.101.242.147:8000/predict/audio"
    if (!audioFile && text) url = "http://100.101.242.147:8000/predict/text"

    try {
      const res = await axios.post(url, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      setResponse(res.data)
    } catch (error) {
      console.error("Error uploading file:", error)
    } finally {
      setIsSubmitting(false)
      setLoadingMessage("")
    }
  }

  return (
    <div className="mx-auto flex w-full flex-col items-center justify-center pt-10">
      <h1 className="mx-auto pb-10 pt-4 text-4xl font-semibold text-[#11111c]">
        Multimodal song Recognition Platform
      </h1>
      <div className="mx-auto w-[full] overflow-hidden rounded-xl bg-white shadow-md">
        <div className="md:flex">
          <div className="p-8">
            <div className="mb-4 text-center text-xl font-bold">
              Upload Audio and Text
            </div>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <input
                  className="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
                  type="file"
                  onChange={handleAudioChange}
                  accept="audio/*"
                />
              </div>
              <div className="mb-6">
                <textarea
                  className="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
                  value={text}
                  onChange={handleTextChange}
                  placeholder="Enter text"
                />
              </div>
              <div className="flex items-center justify-between">
                <button
                  className="focus:shadow-outline rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700 focus:outline-none"
                  type="submit"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "Uploading..." : "Upload"}
                </button>
              </div>
            </form>
            {isSubmitting && (
              <div className="mt-4 text-center text-sm text-gray-500">
                {loadingMessage}
              </div>
            )}
          </div>
        </div>
      </div>
      {response && (
        <div className="mx-auto mt-8 w-[40%]">
          <div className="rounded-md rounded-b border-t-4 border-green-500 bg-green-100 px-4 py-3 text-green-900 shadow-md">
            <div className="mb-4 text-center text-xl font-bold">Response</div>
            <div className="flex justify-between gap-20 font-semibold">
              <div>
                <p className="py-2 text-sm">Song: {response.song}</p>
                <p className="py-2 text-sm">Artist: {response.artist}</p>
                <p className="py-2 text-sm">
                  Confidence: {Math.round(response.confidence * 100)}%
                </p>
              </div>
              <div>
                <a href={response.youtube_url}>
                  <img src={response.thumbnail_url} alt="" width={200} />
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
      {error && (
        <div className="mx-auto mt-8 max-w-md">
          <div className="rounded-b border-t-4 border-red-500 bg-red-100 px-4 py-3 text-red-900 shadow-md">
            <div className="mb-4 text-center text-xl font-bold">Error</div>
            <p className="text-sm">{error}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default UploadPage
