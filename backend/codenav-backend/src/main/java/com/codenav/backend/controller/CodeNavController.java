package com.codenav.backend.controller;

import com.codenav.backend.util.RepoParser;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class CodeNavController {

    // ✅ TEST API
    @GetMapping("/test")
    public String test() {
        return "Backend is working 🚀";
    }

    // ✅ STEP 1: ANALYZE REPO (GET ALL JAVA FILES)
    @GetMapping("/analyzeRepo")
    public List<String> analyzeRepo(@RequestParam String path) {
        return RepoParser.getAllJavaFiles(path);
    }

    // ✅ STEP 2: EXPLAIN PROJECT (ENTRY + STRUCTURE + FLOW)
    @GetMapping("/explain")
    public Map<String, Object> explain(@RequestParam String path) {

        List<String> files = RepoParser.getAllJavaFiles(path);

        Map<String, Object> response = new HashMap<>();

        // 🔹 Entry point detection
        String entryPoint = files.stream()
                .filter(f -> f.contains("Application.java"))
                .findFirst()
                .orElse("Not found");

        // 🔹 Structure
        List<String> structure = List.of(
                "Controllers handle user requests",
                "Services contain business logic"
        );

        // 🔹 Summary
        String summary = "This project follows a layered architecture where requests flow from Controller → Service → Repository.";

        response.put("entryPoint", entryPoint);
        response.put("structure", structure);
        response.put("summary", summary);
        response.put("totalFiles", files.size());

        return response;
    }

    // ✅ STEP 3: Q&A API (AI-like responses)
    @GetMapping("/ask")
    public String ask(@RequestParam String question) {

        question = question.toLowerCase();

        if (question.contains("entry")) {
            return "The entry point is the main Spring Boot application class.";
        }

        if (question.contains("controller")) {
            return "Controllers handle HTTP requests and route them to services.";
        }

        if (question.contains("service")) {
            return "Services contain the business logic of the application.";
        }

        if (question.contains("flow")) {
            return "Request Flow: Controller → Service → Repository.";
        }

        return "Good question! This will be improved with AI soon 🤖";
    }
}