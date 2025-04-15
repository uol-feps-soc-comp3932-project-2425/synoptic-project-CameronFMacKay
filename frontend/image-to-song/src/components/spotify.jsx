import { useState, useEffect } from "react";

export default function Spotify({ songData }) {
  const [currentSong, setCurrentSong] = useState(null);
  const songs = songData?.tag || [];
  const [trackId, setTrackId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [trackDetails, setTrackDetails] = useState(null);

  const API_URL = "http://localhost:8000"; 

  useEffect(() => {
    // Set the first song as current when data is loaded
    if (songs.length > 0) {
      setCurrentSong(songs[0]);
    }
  }, [songData]);

  useEffect(() => {
    // When current song changes, fetch the Spotify track ID
    if (currentSong) {
      fetchSpotifyTrackId(currentSong);
    }
  }, [currentSong]);

  // Function to search for a track on Spotify and get its ID
  const fetchSpotifyTrackId = async (song) => {
    if (!song) return;
    
    setIsLoading(true);
    setError(null);
    setTrackId(null);
    setTrackDetails(null);
    
    try {
      const searchQuery = `${song.title} artist:${song.artist}`;
      
      const response = await fetch(
        `${API_URL}/api/spotify/search?q=${encodeURIComponent(searchQuery)}`
      );
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.tracks && data.tracks.length > 0) {
        const track = data.tracks[0];
        setTrackId(track.id);
        setTrackDetails(track);
      } else {
        setError(`No Spotify tracks found for "${song.title}" by ${song.artist}`);
      }
    } catch (err) {
      console.error("Error fetching Spotify track:", err);
      setError(`Failed to find song on Spotify: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const getSpotifyUrl = () => {
    if (trackDetails && trackDetails.external_urls && trackDetails.external_urls.spotify) {
      return trackDetails.external_urls.spotify;
    }
    
    if (currentSong) {
      const artist = encodeURIComponent(currentSong.artist);
      const title = encodeURIComponent(currentSong.title);
      return `https://open.spotify.com/search/${title}%20artist:${artist}`;
    }
    
    return "";
  };

  if (!songData || songs.length === 0) {
    return (
      <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md w-96">
        <h2 className="text-lg font-semibold mb-4">Spotify Player</h2>
        <p className="text-gray-500">Upload an image to see matching songs</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col p-6 bg-white rounded-lg shadow-md w-96">
      <h2 className="text-lg font-semibold mb-4">Spotify Player</h2>
      
      {currentSong && (
        <div className="mb-4">
          <h3 className="font-bold text-xl">{currentSong.title}</h3>
          <p className="text-gray-600">by {currentSong.artist}</p>
          <p className="text-sm text-gray-500">
            Match score: {(currentSong.overall_similarity * 100).toFixed(1)}
          </p>
        </div>
      )}
      
      {trackDetails && trackDetails.album && trackDetails.album.images && trackDetails.album.images.length > 0 && (
        <div className="mb-4 flex justify-center">
          <img 
            src={trackDetails.album.images[0].url} 
            alt={`${trackDetails.album.name} cover`}
            className="w-48 h-48 object-cover rounded-md shadow-sm"
          />
        </div>
      )}
      
      <div className="w-full h-80 mb-4 bg-gray-50 rounded flex items-center justify-center">
        {isLoading && (
          <div className="text-gray-600">
            Searching for track on Spotify...
          </div>
        )}
        
        {error && (
          <div className="text-red-500 p-4 text-center">
            {error}
          </div>
        )}
        
        {!isLoading && !error && trackId && (
          <iframe
            title="Spotify Web Player"
            src={`https://open.spotify.com/embed/track/${trackId}`}
            width="100%"
            height="100%"
            frameBorder="0"
            allowtransparency="true"
            allow="encrypted-media"
          ></iframe>
        )}
        
        {!isLoading && !error && !trackId && currentSong && !isLoading && (
          <div className="text-gray-600">
            Ready to search for song
          </div>
        )}
      </div>
      
      {trackId && (
        <div className="mt-2 text-center">
          <a
            href={getSpotifyUrl()}
            target="_blank"
            rel="noopener noreferrer"
            className="text-green-600 hover:text-green-800 text-sm font-medium"
          >
            Open in Spotify
          </a>
        </div>
      )}
      
      <div className="mt-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">Select Song:</label>
        <select 
          className="w-full p-2 border rounded"
          onChange={(e) => {
            const selectedIndex = parseInt(e.target.value);
            setCurrentSong(songs[selectedIndex]);
          }}
        >
          {songs.map((song, index) => (
            <option key={index} value={index}>
              {song.artist} - {song.title} ({(song.overall_similarity * 100).toFixed(1)})
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}