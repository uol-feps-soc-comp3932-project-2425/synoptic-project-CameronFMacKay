import { useState } from "react";
import FileUpload from "./components/upload.jsx";
import Lyrics from "./components/lyrics.jsx";
import Spotify from "./components/spotify.jsx";

export default function App() {
  const [songData, setSongData] = useState(null);
  
  return (
    <div className="flex flex-col md:flex-row justify-center items-center gap-6 min-h-screen bg-gray-100 p-4">
      <Spotify songData={songData} />
      <div className="w-full md:w-auto">
        <FileUpload onSongDataReceived={setSongData} />
      </div>
      <div className="flex flex-col md:flex-row gap-6">
        <Lyrics songData={songData} />
      </div>
    </div>
  );
}