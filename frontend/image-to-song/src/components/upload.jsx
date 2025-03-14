import { useState } from "react";
import axios from "axios";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
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
    <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-lg font-semibold mb-4">Upload a File</h2>

      <input type="file" onChange={handleFileChange} className="mb-4" />

      <button onClick={handleUpload} className="px-4 py-2 bg-blue-600 text-white rounded">
        Upload
      </button>

      {message && <p className="mt-4 text-sm">{message}</p>}
    </div>
  );
}
