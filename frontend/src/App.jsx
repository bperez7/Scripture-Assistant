import { useState } from "react";
import { askQuestion } from "./api";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setCitations([]);

    try {
      const result = await askQuestion(question);
      setAnswer(result.answer);
      setCitations(result.citations);
    } catch (error) {
      setAnswer("Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: "800px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>LDS AI Gospel Library</h1>

      <textarea
        rows={4}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a scripture study question..."
        style={{ width: "100%", padding: "12px" }}
      />

      <button onClick={handleAsk} disabled={loading} style={{ marginTop: "12px" }}>
        {loading ? "Studying..." : "Ask"}
      </button>

      {answer && (
        <section style={{ marginTop: "32px" }}>
          <h2>Answer</h2>
          <p style={{ whiteSpace: "pre-wrap" }}>{answer}</p>
        </section>
      )}

      {citations.length > 0 && (
        <section style={{ marginTop: "32px" }}>
          <h2>Scriptures Used</h2>

          {citations.map((citation, index) => (
            <div key={index} style={{ marginBottom: "16px" }}>
              <strong>{citation.reference}</strong>
              <p>{citation.text}</p>
            </div>
          ))}
        </section>
      )}
    </main>
  );
}

export default App;