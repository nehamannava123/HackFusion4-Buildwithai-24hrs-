package com.codenav.backend.controller;

import com.codenav.backend.util.RepoParser;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
public class CodeNavController {

    // 🔹 Test API
    @GetMapping("/test")
    public String test() {
        return "Backend is working 🚀";
    }

    // 🔹 Analyze repo (list Java files)
    @GetMapping("/analyzeRepo")
    public List<String> analyzeRepo(@RequestParam String path) {
        return RepoParser.getAllJavaFiles(path);
    }

    // 🔥 Entry Point Detection
    @GetMapping("/entryPoint")
    public String getEntryPoint(@RequestParam String path) {
        return RepoParser.findEntryPoint(path);
    }
}