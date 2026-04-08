// services/geminiClient.js
// Minimal Gemini API wrapper using the REST endpoint (no SDK needed)

const GEMINI_API_URL =
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent";

/**
 * Calls the Gemini API with a given prompt.
 * Returns the generated text string, or throws on failure.
 */
async function callGemini(prompt) {
  const apiKey = process.env.GEMINI_API_KEY;

  if (!apiKey) {
    throw new Error("GEMINI_API_KEY is not set in environment variables.");
  }

  const response = await fetch(`${GEMINI_API_URL}?key=${apiKey}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [
        {
          parts: [{ text: prompt }],
        },
      ],
      generationConfig: {
        temperature: 0.4,      // balanced: creative but not hallucinating
        maxOutputTokens: 1024,
      },
    }),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Gemini API error ${response.status}: ${errorBody}`);
  }

  const data = await response.json();

  // Extract the text from Gemini's response structure
  const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;

  if (!text) {
    throw new Error("Gemini returned an empty response.");
  }

  return text.trim();
}

module.exports = { callGemini };
