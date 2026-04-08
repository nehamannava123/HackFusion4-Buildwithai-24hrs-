package com.codenav.controller;

import com.codenav.model.CodebaseInfo;
import com.codenav.service.AiLayerService;
import com.codenav.service.RepoParserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*") // Allow frontend to call this
public class CodeNavController {

    @Autowired
    private RepoParserService repoParserService;

    @Autowired
    private AiLayerService aiLayerService;

    // ─────────────────────────────────────────────
    // POST /api/analyze
    // Frontend sends: { repoUrl, level }
    // Returns: explanation + flowSteps from AI layer
    // ─────────────────────────────────────────────
    @PostMapping("/analyze")
    public ResponseEntity<Map<String, Object>> analyze(@RequestBody Map<String, String> request) {
        String repoUrl = request.get("repoUrl");
        String level = request.getOrDefault("level", "beginner");

        if (repoUrl == null || repoUrl.isBlank()) {
            Map<String, Object> error = new HashMap<>();
            error.put("success", false);
            error.put("error", "repoUrl is required");
            return ResponseEntity.badRequest().body(error);
        }

        try {
            // Step 1: Parse the GitHub repo
            CodebaseInfo codebaseInfo = repoParserService.parseRepo(repoUrl, level);

            // Step 2: Send to your Node.js AI layer
            Map<String, Object> aiResponse = aiLayerService.explain(codebaseInfo);

            // Step 3: Add the parsed structure to the response too
            aiResponse.put("parsedStructure", codebaseInfo);

            return ResponseEntity.ok(aiResponse);

        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("success", false);
            error.put("error", "Failed to analyze repo: " + e.getMessage());
            return ResponseEntity.internalServerError().body(error);
        }
    }

    // ─────────────────────────────────────────────
    // POST /api/ask
    // Frontend sends: { question, repoUrl, level }
    // Returns: answer from AI layer
    // ─────────────────────────────────────────────
    @PostMapping("/ask")
    public ResponseEntity<Map<String, Object>> ask(@RequestBody Map<String, String> request) {
        String question = request.get("question");
        String repoUrl = request.get("repoUrl");
        String level = request.getOrDefault("level", "beginner");

        if (question == null || repoUrl == null) {
            Map<String, Object> error = new HashMap<>();
            error.put("success", false);
            error.put("error", "question and repoUrl are required");
            return ResponseEntity.badRequest().body(error);
        }

        try {
            // Re-parse repo to get fresh structure
            CodebaseInfo codebaseInfo = repoParserService.parseRepo(repoUrl, level);

            // Ask the AI layer
            Map<String, Object> aiResponse = aiLayerService.ask(question, codebaseInfo);

            return ResponseEntity.ok(aiResponse);

        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("success", false);
            error.put("error", "Failed to answer: " + e.getMessage());
            return ResponseEntity.internalServerError().body(error);
        }
    }

    // Health check
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> status = new HashMap<>();
        status.put("status", "CodeNav Backend running");
        return ResponseEntity.ok(status);
    }
}
