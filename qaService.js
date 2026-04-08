// services/qaService.js
// Handles /ask endpoint: answers questions about the codebase

const { callGemini } = require("./geminiClient");

// ─────────────────────────────────────────────
// FALLBACK: Rule-based Q&A (no API needed)
// Handles common questions with keyword matching
// ─────────────────────────────────────────────
function fallbackAnswer(question, codebaseJSON) {
  const q = question.toLowerCase();
  const { entryPoint, controllers = [], services = [], repositories = [], flow = [] } = codebaseJSON;

  if (q.includes("entry") || q.includes("start") || q.includes("begin") || q.includes("main")) {
    return `The application starts at "${entryPoint}". This is where execution begins when the app launches.`;
  }

  if (q.includes("controller")) {
    return controllers.length
      ? `The controllers in this project are: ${controllers.join(", ")}. Controllers handle incoming HTTP requests and route them to the appropriate service.`
      : "No controllers were found in this codebase.";
  }

  if (q.includes("service")) {
    return services.length
      ? `The services in this project are: ${services.join(", ")}. Services contain the core business logic of the application.`
      : "No services were found in this codebase.";
  }

  if (q.includes("database") || q.includes("repository") || q.includes("data")) {
    return repositories.length
      ? `Database access is handled by: ${repositories.join(", ")}. Repositories are responsible for querying and persisting data.`
      : "No repositories were found in this codebase.";
  }

  if (q.includes("flow") || q.includes("how") || q.includes("work") || q.includes("login")) {
    return flow.length
      ? `Here's how the application flows:\n${flow.map((f, i) => `  Step ${i + 1}: ${f}`).join("\n")}`
      : "No flow information is available for this codebase.";
  }

  // Generic fallback
  return `Based on the codebase structure:
- Entry Point: ${entryPoint || "Not specified"}
- Controllers: ${controllers.join(", ") || "None"}
- Services: ${services.join(", ") || "None"}
- Repositories: ${repositories.join(", ") || "None"}

Could you rephrase your question? Try asking about controllers, services, repositories, or the application flow.`;
}

// ─────────────────────────────────────────────
// answerQuestion: calls Gemini or falls back
// ─────────────────────────────────────────────
async function answerQuestion(question, codebaseJSON) {
  const prompt = `
You are CodeNav AI, an expert at explaining codebases to developers.

Here is the structure of the codebase:
${JSON.stringify(codebaseJSON, null, 2)}

A developer is asking: "${question}"

Answer clearly and helpfully based ONLY on the provided codebase structure.
- If the answer is in the structure, explain it step by step.
- If the question asks about a flow (e.g., "how does login work?"), trace through the relevant components.
- Keep your answer under 200 words.
- Do not make up components that are not in the JSON.
`.trim();

  try {
    const result = await callGemini(prompt);
    return result;
  } catch (err) {
    console.warn("⚠️  Gemini unavailable, using fallback Q&A:", err.message);
    return fallbackAnswer(question, codebaseJSON);
  }
}

module.exports = { answerQuestion };
