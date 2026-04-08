package com.codenav.model;

import java.util.List;

public class CodebaseInfo {

    private String repoUrl;
    private String entryPoint;
    private List<String> controllers;
    private List<String> services;
    private List<String> repositories;
    private List<String> flow;
    private String level; // beginner | intermediate | advanced

    public CodebaseInfo() {}

    public String getRepoUrl() { return repoUrl; }
    public void setRepoUrl(String repoUrl) { this.repoUrl = repoUrl; }

    public String getEntryPoint() { return entryPoint; }
    public void setEntryPoint(String entryPoint) { this.entryPoint = entryPoint; }

    public List<String> getControllers() { return controllers; }
    public void setControllers(List<String> controllers) { this.controllers = controllers; }

    public List<String> getServices() { return services; }
    public void setServices(List<String> services) { this.services = services; }

    public List<String> getRepositories() { return repositories; }
    public void setRepositories(List<String> repositories) { this.repositories = repositories; }

    public List<String> getFlow() { return flow; }
    public void setFlow(List<String> flow) { this.flow = flow; }

    public String getLevel() { return level; }
    public void setLevel(String level) { this.level = level; }
}