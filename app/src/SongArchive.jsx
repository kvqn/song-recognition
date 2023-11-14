import axios from "axios"
import { useEffect, useState } from "react"

export default function SongArchive() {
  const [songs, setSongs] = useState([])
  const [filter, setFilter] = useState("")
  const [filteredSongs, setFilteredSongs] = useState([])

  useEffect(() => {
    async function _() {
      const resp = await axios.get("http://100.101.242.147:8000/songs")
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

  // console.log(filteredSongs)
  return (
    <div className="flex flex-row justify-center">
      <div className="flex w-1/2 flex-col justify-evenly gap-2">
        <input
          type="text"
          className="mt-8 border-2 p-2"
          onChange={onFilterChange}
          placeholder="Search Songs"
        ></input>
        <div className="mb-8 flex flex-col items-center">
          <p>{filteredSongs.length} results</p>
        </div>
        {filteredSongs.map((song, i) => (
          <div
            key={i}
            className="flex w-full flex-row items-center justify-between rounded-[0.5rem] border-2 bg-gray-50 p-4 transition-all hover:scale-[1.01] hover:border-black hover:bg-[#bac2c4]"
          >
            <div>
              <div className="font-bold">{song.song}</div>
              <div>{song.artist}</div>
            </div>
            <a href={song.youtube_url} target="_blank">
              <img src={song.thumbnail_url} width={200} height={150}></img>
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}
