// services/explainService.js
// Handles /explain endpoint: generates codebase explanation + flow steps

const { callGemini } = require("./geminiClient");

// ─────────────────────────────────────────────
// FALLBACK: Template-based explanation
// Used when Gemini API is unavailable
// ─────────────────────────────────────────────
function fallbackExplanation(codebaseJSON) {
  const { entryPoint, controllers = [], services = [], repositories = [], flow = [] } = codebaseJSON;

  return `
📌 Entry Point: ${entryPoint || "Not specified"}

🎮 Controllers (handle HTTP requests):
${controllers.length ? controllers.map((c) => `  • ${c}`).join("\n") : "  None found"}

⚙️  Services (contain business logic):
${services.length ? services.map((s) => `  • ${s}`).join("\n") : "  None found"}

🗄️  Repositories (talk to the database):
${repositories.length ? repositories.map((r) => `  • ${r}`).join("\n") : "  None found"}

🔄 Application Flow:
${flow.length ? flow.map((f, i) => `  Step ${i + 1}: ${f}`).join("\n") : "  No flow defined"}

Note: This is a template-based explanation. Gemini API was unavailable.
`.trim();
}

// ─────────────────────────────────────────────
// LEVEL-SPECIFIC prompt instructions
// ─────────────────────────────────────────────
const levelInstructions = {
  beginner:
    "Explain this as if talking to a complete beginner. Avoid jargon. Use simple words and short sentences. Add helpful analogies.",
  intermediate:
    "Explain this for a developer with basic programming knowledge. Use correct terminology but still clarify architectural patterns.",
  advanced:
    "Explain this for an experienced developer. Be concise and technical. Mention design patterns, architectural decisions, and trade-offs.",
};

// ─────────────────────────────────────────────
// explainCodebase: calls Gemini or falls back
// ─────────────────────────────────────────────
async function explainCodebase(codebaseJSON, level = "beginner") {
  const instruction = levelInstructions[level] || levelInstructions.beginner;

  const prompt = `
You are CodeNav AI, an expert at helping developers understand codebases.

${instruction}

Here is the structure of a codebase in JSON format:
${JSON.stringify(codebaseJSON, null, 2)}

Your task:
1. Briefly explain what this application does based on its structure.
2. Describe the role of each component (controllers, services, repositories).
3. Explain how the components connect to each other.
4. Point out where a developer should start reading the code.

Keep your response clear, structured, and under 300 words.
`.trim();

  try {
    const result = await callGemini(prompt);
    return result;
  } catch (err) {
    console.warn("⚠️  Gemini unavailable, using fallback explanation:", err.message);
    return fallbackExplanation(codebaseJSON);
  }
}

// ─────────────────────────────────────────────
// simulateFlow: converts flow array → numbered steps
// Pure logic, no API call needed
// ─────────────────────────────────────────────
function simulateFlow(flow = []) {
  if (!flow.length) {
    return ["No flow data provided."];
  }

  return flow.map((step, index) => {
    const [from, to] = step.split("->").map((s) => s.trim());

    if (!to) {
      return `Step ${index + 1}: ${from}`;
    }

    // Make step human-readable based on component type
    const action = getActionVerb(from, to);
    return `Step ${index + 1}: ${from} ${action} ${to}`;
  });
}

// Returns a contextual verb based on component names
function getActionVerb(from, to) {
  const fromLower = from.toLowerCase();
  const toLower = to.toLowerCase();

  if (fromLower.includes("controller")) return "forwards the request to";
  if (fromLower.includes("service") && toLower.includes("repository")) return "queries the database via";
  if (fromLower.includes("service")) return "delegates business logic to";
  if (fromLower.includes("repository")) return "fetches data using";
  return "calls";
}

module.exports = { explainCodebase, simulateFlow };
