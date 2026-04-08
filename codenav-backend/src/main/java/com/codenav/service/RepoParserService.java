package main.java.com.codenav.service;

import com.codenav.model.CodebaseInfo;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;

@Service
public class RepoParserService {

    private final HttpClient httpClient = HttpClient.newHttpClient();
    private final ObjectMapper objectMapper = new ObjectMapper();

    // ─────────────────────────────────────────────
    // Main method: parse a GitHub URL into CodebaseInfo
    // ─────────────────────────────────────────────
    public CodebaseInfo parseRepo(String repoUrl, String level) throws IOException, InterruptedException {
        // Convert GitHub URL to API URL
        // e.g. https://github.com/user/repo → https://api.github.com/repos/user/repo/contents
        String apiUrl = convertToApiUrl(repoUrl);

        // Fetch top-level file list from GitHub API
        List<String> allFiles = fetchFileList(apiUrl, "");

        CodebaseInfo info = new CodebaseInfo();
        info.setRepoUrl(repoUrl);
        info.setLevel(level != null ? level : "beginner");

        // Detect components by scanning filenames
        info.setEntryPoint(detectEntryPoint(allFiles));
        info.setControllers(detectByPattern(allFiles, "Controller"));
        info.setServices(detectByPattern(allFiles, "Service"));
        info.setRepositories(detectByPattern(allFiles, "Repository", "Repo"));
        info.setFlow(buildFlow(info.getControllers(), info.getServices(), info.getRepositories()));

        return info;
    }

    // ─────────────────────────────────────────────
    // Convert GitHub web URL → GitHub API URL
    // ─────────────────────────────────────────────
    private String convertToApiUrl(String repoUrl) {
        // Remove trailing slash
        repoUrl = repoUrl.trim().replaceAll("/$", "");
        // https://github.com/user/repo → https://api.github.com/repos/user/repo/contents
        return repoUrl
                .replace("https://github.com/", "https://api.github.com/repos/")
                + "/contents";
    }

    // ─────────────────────────────────────────────
    // Fetch file list recursively from GitHub API
    // Limited to 2 levels deep to keep it fast
    // ─────────────────────────────────────────────
    private List<String> fetchFileList(String baseApiUrl, String path) throws IOException, InterruptedException {
        List<String> files = new ArrayList<>();
        String url = path.isEmpty() ? baseApiUrl : baseApiUrl + "/" + path;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Accept", "application/vnd.github.v3+json")
                .header("User-Agent", "CodeNav-AI")
                .GET()
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() != 200) {
            return files; // Return empty if API fails
        }

        JsonNode items = objectMapper.readTree(response.body());

        if (items.isArray()) {
            for (JsonNode item : items) {
                String name = item.get("name").asText();
                String type = item.get("type").asText();
                String itemPath = path.isEmpty() ? name : path + "/" + name;

                if (type.equals("file")) {
                    files.add(name);
                } else if (type.equals("dir")) {
                    // Only go one level deep into src folders
                    if (name.equals("src") || name.equals("main") || name.equals("java")
                            || name.equals("controller") || name.equals("service")
                            || name.equals("repository") || name.equals("model")) {
                        files.addAll(fetchFileList(baseApiUrl, itemPath));
                    }
                }
            }
        }

        return files;
    }

    // ─────────────────────────────────────────────
    // Detect entry point (main class or index file)
    // ─────────────────────────────────────────────
    private String detectEntryPoint(List<String> files) {
        String[] entryPatterns = {
            "Application.java", "Main.java", "App.java",
            "index.js", "main.py", "app.py", "index.ts",
            "Program.cs", "main.go"
        };

        for (String pattern : entryPatterns) {
            for (String file : files) {
                if (file.endsWith(pattern)) return file;
            }
        }

        // Fallback: anything with "Application" in the name
        for (String file : files) {
            if (file.contains("Application") && file.endsWith(".java")) return file;
        }

        return files.isEmpty() ? "Not detected" : files.get(0);
    }

    // ─────────────────────────────────────────────
    // Detect files matching given keyword patterns
    // ─────────────────────────────────────────────
    private List<String> detectByPattern(List<String> files, String... patterns) {
        List<String> matched = new ArrayList<>();
        for (String file : files) {
            for (String pattern : patterns) {
                if (file.contains(pattern) && !matched.contains(file)) {
                    matched.add(file);
                }
            }
        }
        return matched;
    }

    // ─────────────────────────────────────────────
    // Build a simple flow array from detected components
    // e.g. ["AuthController -> AuthService", "AuthService -> UserRepository"]
    // ─────────────────────────────────────────────
    private List<String> buildFlow(List<String> controllers, List<String> services, List<String> repos) {
        List<String> flow = new ArrayList<>();

        // Match controllers to services by name prefix
        for (String controller : controllers) {
            String prefix = controller.replace("Controller.java", "").replace("Controller", "");
            for (String service : services) {
                if (service.contains(prefix)) {
                    String controllerName = controller.replace(".java", "");
                    String serviceName = service.replace(".java", "");
                    flow.add(controllerName + " -> " + serviceName);
                }
            }
        }

        // Match services to repositories by name prefix
        for (String service : services) {
            String prefix = service.replace("Service.java", "").replace("Service", "");
            for (String repo : repos) {
                if (repo.contains(prefix)) {
                    String serviceName = service.replace(".java", "");
                    String repoName = repo.replace(".java", "");
                    flow.add(serviceName + " -> " + repoName);
                }
            }
        }

        // If no flow detected, add generic ones
        if (flow.isEmpty()) {
            if (!controllers.isEmpty() && !services.isEmpty()) {
                flow.add(controllers.get(0).replace(".java", "") + " -> " + services.get(0).replace(".java", ""));
            }
            if (!services.isEmpty() && !repos.isEmpty()) {
                flow.add(services.get(0).replace(".java", "") + " -> " + repos.get(0).replace(".java", ""));
            }
        }

        return flow;
    }
}
