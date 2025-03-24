import { useState } from "react";
import axios from "axios";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      console.log(response.data.image_data);
      setMessage(JSON.stringify(response.data.image_data, null, 2));
    } catch (error) {
      setMessage("Upload failed!");
    }
  };

  return (
    <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md w-96">
      <h2 className="text-lg font-semibold mb-4">Upload a File</h2>
      
      <input type="file" onChange={handleFileChange} className="mb-4" />
      
      {preview && (
        <img src={preview} alt="Preview" className="w-32 h-32 object-cover mb-4 border rounded" />
      )}
      
      <button onClick={handleUpload} className="px-4 py-2 bg-blue-600 text-white rounded">
        Upload
      </button>
      
      {message && <pre className="mt-4 text-sm bg-gray-100 p-2 rounded w-full text-left overflow-auto">{message}</pre>}
    </div>
  );
}
