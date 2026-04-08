package com.codenav.backend.service;

import com.codenav.backend.util.RepoParser;
import com.codenav.backend.model.ExplanationResponse;

import java.util.ArrayList;
import java.util.List;

public class ExplanationService {

    public static ExplanationResponse explainRepo(String path) {

        List<String> files = RepoParser.getAllJavaFiles(path);
        List<String> entry = RepoParser.findEntryPoint(path);
        List<String> flow = RepoParser.findControllerServiceFlow(path);

        String entryPoint = entry.isEmpty() ? "Not found" : entry.get(0);

        List<String> structure = new ArrayList<>();

        boolean hasController = false;
        boolean hasService = false;
        boolean hasRepo = false;

        for (String f : flow) {
            if (f.contains("Controller")) hasController = true;
            if (f.contains("Service")) hasService = true;
            if (f.contains("Repository")) hasRepo = true;
        }

        if (hasController) structure.add("Controllers handle user requests");
        if (hasService) structure.add("Services contain business logic");
        if (hasRepo) structure.add("Repositories manage database operations");

        String summary = "This project follows a layered architecture where requests flow from Controller → Service → Repository.";

        return new ExplanationResponse(entryPoint, structure, summary, files.size());
    }
}