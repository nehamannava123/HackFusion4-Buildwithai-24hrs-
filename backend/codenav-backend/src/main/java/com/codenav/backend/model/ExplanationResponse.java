package com.codenav.backend.model;

import java.util.List;

public class ExplanationResponse {

    public String entryPoint;
    public List<String> structure;
    public String summary;
    public int totalFiles;

    public ExplanationResponse(String entryPoint, List<String> structure, String summary, int totalFiles) {
        this.entryPoint = entryPoint;
        this.structure = structure;
        this.summary = summary;
        this.totalFiles = totalFiles;
    }
}