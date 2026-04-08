package com.codenav.backend.controller;

import com.codenav.backend.util.RepoParser;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
public class CodeNavController {

    // ✅ Test API
    @GetMapping("/test")
    public String test() {
        return "Backend is working 🚀";
    }

    // ✅ Get all Java files
    @GetMapping("/analyzeRepo")
    public List<String> analyzeRepo(@RequestParam String path) {
        return RepoParser.getAllJavaFiles(path);
    }

    // ✅ Get entry point
    @GetMapping("/entryPoint")
    public List<String> entryPoint(@RequestParam String path) {
        return RepoParser.findEntryPoint(path);
    }

    // ✅ Get architecture flow
    @GetMapping("/flow")
    public List<String> getFlow(@RequestParam String path) {
        return RepoParser.findControllerServiceFlow(path);
    }
}