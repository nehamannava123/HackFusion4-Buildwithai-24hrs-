package com.codenav.backend.service;

import com.codenav.backend.util.RepoParser;

import java.util.List;

public class QnAService {

    public static String answerQuestion(String path, String question) {

        question = question.toLowerCase();

        List<String> files = RepoParser.getAllJavaFiles(path);
        List<String> entry = RepoParser.findEntryPoint(path);
        List<String> flow = RepoParser.findControllerServiceFlow(path);

        // 🔹 What does project do?
        if (question.contains("what") && question.contains("project")) {
            return "This project is a Spring Boot backend that analyzes repositories and explains their structure.";
        }

        // 🔹 Entry point
        if (question.contains("entry") || question.contains("start")) {
            return entry.isEmpty() ? "No entry point found" : "Project starts from: " + entry.get(0);
        }

        // 🔹 Structure
        if (question.contains("structure") || question.contains("architecture")) {
            return "This project follows Controller → Service → Repository architecture.";
        }

        // 🔹 File count
        if (question.contains("files")) {
            return "Total Java files: " + files.size();
        }

        // 🔹 Default
        return "Sorry, I don't understand the question yet.";
    }
}