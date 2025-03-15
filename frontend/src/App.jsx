import { useState } from "react";
import axios from "axios";

function App() {
  const [channelId, setChannelId] = useState("");
  const [userInput, setUserInput] = useState("");
  const [analysis, setAnalysis] = useState("");

  const fetchAnalysis = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze", {
        channelId,
        userInput,
      });
      setAnalysis(response.data.analysis);
    } catch (error) {
      console.error("Error fetching analysis:", error);
    }
  };

  return (
    <div>
      <h1>YouTube Comment Analyzer</h1>
      <input
        type="text"
        placeholder="Enter YouTube Channel ID"
        value={channelId}
        onChange={(e) => setChannelId(e.target.value)}
      />
      <input
        type="text"
        placeholder="Enter analysis prompt"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
      />
      <button onClick={fetchAnalysis}>Analyze Comments</button>
      <h2>Analysis Result:</h2>
      <p>{analysis}</p>
    </div>
  );
}

export default App;
