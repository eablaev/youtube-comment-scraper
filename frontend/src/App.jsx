import { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchAnalysis = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze", {
        userInput: prompt,
      });

      setAnalysis(response.data.analysis);
    } catch (error) {
      console.error("Error fetching analysis:", error);
      setAnalysis("Failed to get analysis.");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>YouTube Comment Analyzer</h1>
      
      <textarea
        rows="3"
        cols="50"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your analysis prompt"
      />
      <br />
      
      <button onClick={fetchAnalysis} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Comments"}
      </button>

      <h2>Analysis:</h2>
      <p>{analysis}</p>
    </div>
  );
}

export default App;
