import { useState } from "react";
import axios from "axios";

export default function FileUpload({ onSongDataReceived }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [songData, setSongData] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setError("");
      setSongData(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first!");
      return;
    }

    setLoading(true);
    setError("");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      
      let processedData = response.data.image_data;
      
      // Process the data to ensure it's in the right format and includes lyrics
      if (processedData) {
        // If it's an array, process each item
        if (Array.isArray(processedData)) {
          processedData = processedData.map(song => {
            // Remove any tag property if it exists
            const { tag, ...rest } = song;
            return rest;
          });
        } else if (typeof processedData === 'object') {
          // If it's a single object, remove tag property
          const { tag, ...rest } = processedData;
          processedData = rest;
        }
        
        // Pass the processed data to the parent component
        onSongDataReceived(response.data.image_data);
        setSongData(processedData);
        console.log(processedData);
      }
      
      setLoading(false);
    } catch (error) {
      setError("Upload failed! " + (error.response?.data?.detail || error.message));
      setLoading(false);
      onSongDataReceived(null);
      setSongData(null);
    }
  };

  return (
    <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md w-full max-w-md">
      <h2 className="text-lg font-semibold mb-4">Find Songs by Image</h2>
      
      <input 
        type="file" 
        onChange={handleFileChange} 
        className="mb-4 w-full text-sm text-gray-500
          file:mr-4 file:py-2 file:px-4
          file:rounded file:border-0
          file:text-sm file:font-semibold
          file:bg-blue-50 file:text-blue-700
          hover:file:bg-blue-100"
        accept="image/*"
      />
      
      {preview && (
        <img src={preview} alt="Preview" className="w-256 h-256 object-cover mb-4 border rounded" />
      )}
      
      <button 
        onClick={handleUpload} 
        className="px-4 py-2 bg-blue-600 text-white rounded w-full hover:bg-blue-700 transition"
        disabled={loading}
      >
        {loading ? "Processing..." : "Find Matching Songs"}
      </button>
      
      {error && <p className="mt-4 text-sm text-red-500">{error}</p>}
    </div>
  );
}