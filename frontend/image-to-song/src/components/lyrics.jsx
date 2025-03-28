import { useState, useEffect } from "react";

export default function Lyrics({ songData }) {
  const [currentSong, setCurrentSong] = useState(null);
  const songs = songData?.tag || [];

  useEffect(() => {
    // Set the first song as current when data is loaded
    if (songs.length > 0) {
      setCurrentSong(songs[0]);
    }
  }, [songData]);

  // Handle song selection
  const handleSelectSong = (song) => {
    setCurrentSong(song);
  };

  if (!songData || songs.length === 0) {
    return (
      <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md w-96">
        <h2 className="text-lg font-semibold mb-4">Song Lyrics</h2>
        <p className="text-gray-500">Upload an image to see matching lyrics</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col p-6 bg-white rounded-lg shadow-md w-96 max-h-[600px] overflow-hidden">
      <h2 className="text-lg font-semibold mb-4">Song Lyrics</h2>
      
      {/* Image information */}
      <div className="mb-4 text-sm text-gray-600">
      <p>Image Class: {songData.image}</p>
        <p>Brightness: {songData.brightness?.toFixed(1)}(0-255)</p>
        <p>Contrast: {songData.contrast?.toFixed(1)}(0-255)</p>
        {songData.main_colour && (
          <p>Main color: rgb({songData.main_colour.join(', ')})</p>
        )}
      </div>
      
      {/* Song selector */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">Select Song:</label>
        <select 
          className="w-full p-2 border rounded"
          onChange={(e) => {
            const selectedIndex = parseInt(e.target.value);
            handleSelectSong(songs[selectedIndex]);
          }}
        >
          {songs.map((song, index) => (
            <option key={index} value={index}>
              {song.artist} - {song.title} ({(song.overall_similarity * 100).toFixed(1)})
            </option>
          ))}
        </select>
      </div>
      
      {/* Current song details */}
      {currentSong && (
        <div>
          <div className="mb-4">
            <h3 className="font-bold text-xl">{currentSong.title}</h3>
            <p className="text-gray-600">by {currentSong.artist}</p>
            <p className="text-sm text-gray-500">
              Match score: {(currentSong.overall_similarity * 100).toFixed(1)}
            </p>
          </div>
          
          {/* Lyrics with highlighting */}
          <div className="overflow-y-auto max-h-96 p-2 bg-gray-50 rounded">
            {currentSong.lyrics.map((line, lineIndex) => {
              // If there are no matches in this line, just display the text
              if (!line.words || line.words.length === 0) {
                return <p key={lineIndex} className="mb-1">{line.text}</p>;
              }
              
              // For lines with matches, we need to highlight the matching words
              let currentIndex = 0;
              const lineElements = [];
              const sortedWords = [...line.words].sort((a, b) => a.start_idx - b.start_idx);
              console.log(sortedWords)
              // Split the line text into words to apply highlighting
              const words = line.text.split(' ');
              
              sortedWords.forEach((match, matchIndex) => {
                // Get the start and end word indices
                const startWordIdx = match.start_idx;
                const endWordIdx = match.end_idx;
                
                // Add any non-highlighted text before this match
                if (startWordIdx > currentIndex) {
                  lineElements.push(
                    <span key={`pre-${lineIndex}-${matchIndex}`}>
                      {words.slice(currentIndex, startWordIdx).join(' ')}{' '}
                    </span>
                  );
                }
                
                // Add the highlighted text
                const highlightStyle = {
                  backgroundColor: 
                    match.strength === "strong" ? "rgb(26, 255, 0)" :
                    match.strength === "medium" ? "rgb(255, 221, 0)" : 
                    "rgb(255, 0, 0)",
                  padding: "0 2px",
                  borderRadius: "2px",
                  display: "inline"
                };
                
                lineElements.push(
                  <span 
                    key={`match-${lineIndex}-${matchIndex}`} 
                    style={highlightStyle}
                    title={`Match strength: ${match.strength} (${(match.similarity * 100).toFixed(1)})`}
                  >
                    {words.slice(startWordIdx, endWordIdx + 1).join(' ')}
                  </span>
                );
                
                // Add a space after the highlight
                lineElements.push(<span key={`space-${lineIndex}-${matchIndex}`}>{' '}</span>);
                
                // Update current index
                currentIndex = endWordIdx + 1;
              });
              
              // Add any remaining text after the last match
              if (currentIndex < words.length) {
                lineElements.push(
                  <span key={`post-${lineIndex}`}>
                    {words.slice(currentIndex).join(' ')}
                  </span>
                );
              }
              
              return <p key={lineIndex} className="mb-1">{lineElements}</p>;
            })}
          </div>
        </div>
      )}
    </div>
  );
}