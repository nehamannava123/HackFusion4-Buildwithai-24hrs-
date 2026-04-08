# CodeNav AI — Node.js AI Layer

AI-powered codebase explanation engine using Google Gemini API.

## Setup

```bash
npm install
cp .env.example .env
# Add your GEMINI_API_KEY to .env
npm start
```

## API Endpoints

### POST /explain
Generates a human-readable explanation of a codebase + flow steps.

**Request:**
```json
{
  "codebaseJSON": {
    "entryPoint": "Application.java",
    "controllers": ["AuthController"],
    "services": ["AuthService"],
    "repositories": ["UserRepository"],
    "flow": ["AuthController -> AuthService", "AuthService -> UserRepository"]
  },
  "level": "beginner"
}
```
`level` options: `"beginner"` | `"intermediate"` | `"advanced"`

**Response:**
```json
{
  "success": true,
  "level": "beginner",
  "explanation": "This application...",
  "flowSteps": [
    "Step 1: AuthController forwards the request to AuthService",
    "Step 2: AuthService queries the database via UserRepository"
  ]
}
```

---

### POST /ask
Answers a specific question about the codebase.

**Request:**
```json
{
  "question": "How does login work?",
  "codebaseJSON": { ... }
}
```

**Response:**
```json
{
  "success": true,
  "question": "How does login work?",
  "answer": "When a user logs in..."
}
```

## Fallback Behavior
If the Gemini API is unavailable (rate limit, no key, network error), the system automatically falls back to template-based and rule-based responses. The API will never crash — it always returns something useful.

## Project Structure
```
codenav-ai/
├── server.js                  # Express app, routes
├── services/
│   ├── geminiClient.js        # Gemini API wrapper
│   ├── explainService.js      # Explanation + flow simulation
│   └── qaService.js           # Context-aware Q&A
├── .env.example               # Environment variable template
└── package.json
```
