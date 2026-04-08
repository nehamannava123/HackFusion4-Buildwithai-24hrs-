const express = require("express");
const cors = require("cors");
const { explainCodebase, simulateFlow } = require("./services/explainService");
const { answerQuestion } = require("./services/qaService");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// ─────────────────────────────────────────────
// POST /explain
// Body: { codebaseJSON, level? }
// level: "beginner" | "intermediate" | "advanced"
// ─────────────────────────────────────────────
app.post("/explain", async (req, res) => {
  const { codebaseJSON, level = "beginner" } = req.body;

  if (!codebaseJSON) {
    return res.status(400).json({ error: "codebaseJSON is required." });
  }

  try {
    const explanation = await explainCodebase(codebaseJSON, level);
    const flowSteps = simulateFlow(codebaseJSON.flow || []);

    return res.json({
      success: true,
      level,
      explanation,
      flowSteps,
    });
  } catch (err) {
    console.error("Error in /explain:", err.message);
    return res.status(500).json({ error: "Something went wrong.", details: err.message });
  }
});

// ─────────────────────────────────────────────
// POST /ask
// Body: { question, codebaseJSON }
// ─────────────────────────────────────────────
app.post("/ask", async (req, res) => {
  const { question, codebaseJSON } = req.body;

  if (!question || !codebaseJSON) {
    return res.status(400).json({ error: "Both question and codebaseJSON are required." });
  }

  try {
    const answer = await answerQuestion(question, codebaseJSON);
    return res.json({ success: true, question, answer });
  } catch (err) {
    console.error("Error in /ask:", err.message);
    return res.status(500).json({ error: "Something went wrong.", details: err.message });
  }
});

// Health check
app.get("/", (req, res) => {
  res.json({ status: "CodeNav AI is running 🚀" });
});

app.listen(PORT, () => {
  console.log(`✅ CodeNav AI server running on http://localhost:${PORT}`);
});
