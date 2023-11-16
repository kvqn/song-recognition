import { useState } from "react"
import axios from "axios"
import { useReactMediaRecorder } from "react-media-recorder"
import { twMerge } from "tailwind-merge"
// import { useAudioRecorder } from "react-audio-voice-recorder"
import { useEffect } from "react"

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

const UploadPage = () => {
  const [audioFile, setAudioFile] = useState(null)
  const [text, setText] = useState("")
  const [response, setResponse] = useState(null)
  const [loadingMessage, setLoadingMessage] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)

  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ audio: true })

  // const {
  //   startRecording,
  //   stopRecording,
  //   // togglePauseResume,
  //   recordingBlob,
  //   isRecording,
  //   isPaused,
  //   recordingTime,
  //   // mediaRecorder,
  // } = useAudioRecorder()

  const [onRecordTab, setOnRecordTab] = useState(false)

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

    let file

    if (!onRecordTab) {
      if (!audioFile && !text) {
        setError("Please upload an audio file or enter text")
        return
      }
      file = audioFile
    } else {
      if (!mediaBlobUrl && !text) {
        setError("Please record an audio file or enter text")
        return
      }
      if (mediaBlobUrl) {
        const resp = await fetch(mediaBlobUrl)
        const recordingBlob = await resp.blob()
        file = new File([recordingBlob], "audio.wav", { type: "audio/wav" })
      }
    }

    setError(null)

    setIsSubmitting(true)
    cycleLoadingMessages()

    const formData = new FormData()
    console.log(file)
    if (file) formData.append("audio", file)
    if (text) formData.append("text", text)

    let url
    if (file && text) url = "http://100.101.242.147:8000/predict/audio-and-text"
    if (file && !text) url = "http://100.101.242.147:8000/predict/audio"
    if (!file && text) url = "http://100.101.242.147:8000/predict/text"

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

      <div className="w-1/2 overflow-hidden rounded-xl bg-white shadow-md">
        <div className="">
          <div className="flex h-12 justify-evenly border-b-2">
            <div
              className={twMerge(
                "flex h-full w-full items-center justify-center border-r transition-all",
                onRecordTab ? "hover:bg-blue-100" : "bg-blue-200",
              )}
              onClick={() => {
                setOnRecordTab(false)
              }}
            >
              Upload File
            </div>
            <div
              className={twMerge(
                "flex h-full w-full items-center justify-center border-r transition-all hover:bg-blue-100",
                onRecordTab ? "bg-blue-200" : "hover:bg-blue-100",
              )}
              onClick={() => {
                setOnRecordTab(true)
              }}
            >
              Record Audio
            </div>
          </div>
          <div className="p-8">
            <div className="mb-4 text-center text-xl font-bold">
              {onRecordTab ? "Record Audio and Text" : "Upload File and Text"}
            </div>
            <div>
              {onRecordTab ? (
                <div className="flex justify-center gap-4 p-4">
                  <button
                    onClick={async () => {
                      startRecording()
                      await sleep(5000)
                      stopRecording()
                    }}
                    className={twMerge(
                      "block rounded-3xl bg-red-500 px-4 py-2 font-bold text-white hover:bg-red-700 focus:outline-none",
                      status === "recording" ? "bg-blue-500" : "",
                    )}
                    disabled={status === "recording"}
                  >
                    {status === "recording"
                      ? "Recording.."
                      : " Start Recording "}
                  </button>
                  <audio className="block" src={mediaBlobUrl} controls />
                </div>
              ) : (
                <div className="mb-4">
                  <input
                    className="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
                    type="file"
                    onChange={handleAudioChange}
                    accept="audio/*"
                  />
                </div>
              )}
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
                  onClick={handleSubmit}
                >
                  {isSubmitting ? "Uploading..." : "Upload"}
                </button>
              </div>
            </div>
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
