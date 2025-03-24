import { useState } from "react";
import FileUpload from "./components/upload.jsx";
import Lyrics from "./components/lyrics.jsx";

export default function App() {
  const [songData, setSongData] = useState(null);
  
  return (
    <div className="flex justify-center items-center gap-6 min-h-screen bg-gray-100 p-4">
      <FileUpload onSongDataReceived={setSongData} />
      <Lyrics songData={songData} />
    </div>
  );
}