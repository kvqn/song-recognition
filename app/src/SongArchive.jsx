import axios from "axios"
import { useEffect, useState } from "react"

export default function SongArchive() {
  const [songs, setSongs] = useState([])
  const [filter, setFilter] = useState("")
  const [filteredSongs, setFilteredSongs] = useState([])

  useEffect(() => {
    async function _() {
      const resp = await axios.get("http://localhost:8000/songs")
      setSongs(resp.data.songs)
    }
    _()
  }, [])

  function onFilterChange(e) {
    e.preventDefault()
    const filter = e.target.value.toLowerCase()
    setFilter(filter)
  }

  useEffect(() => {
    if (filter === "") setFilteredSongs(songs)
    else {
      const filtered = songs.filter((song) => {
        return (
          song.song.toLowerCase().includes(filter) ||
          song.artist.toLowerCase().includes(filter)
        )
      })
      setFilteredSongs(filtered)
    }
  }, [filter, songs])

  return (
    <div className="flex flex-row justify-center">
      <div className="flex w-1/2 flex-col justify-evenly gap-2">
        <input
          type="text"
          className="mt-8 border-2 p-2"
          onChange={onFilterChange}
          placeholder="Search"
        ></input>
        <div className="mb-8 flex flex-col items-center">
          <p>{filteredSongs.length} results</p>
        </div>
        {filteredSongs.map((song, i) => (
          <div
            key={i}
            className="flex w-full flex-row items-center justify-between border-2 p-4 transition-all hover:border-black"
          >
            <div>
              <div className="font-bold">{song.song}</div>
              <div>{song.artist}</div>
            </div>
            <a href={song.youtube_url}>
              <img src={song.thumbnail_url} width={200}></img>
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}
