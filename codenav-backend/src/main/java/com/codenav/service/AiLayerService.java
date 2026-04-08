package main.java.com.codenav.service;

import com.codenav.model.CodebaseInfo;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.HashMap;
import java.util.Map;

@Service
public class AiLayerService {

    // Your Node.js AI layer URL — set in application.properties
    @Value("${ai.layer.url:http://localhost:3000}")
    private String aiLayerUrl;

    private final HttpClient httpClient = HttpClient.newHttpClient();
    private final ObjectMapper objectMapper = new ObjectMapper();

    // ─────────────────────────────────────────────
    // Call /explain on your Node.js AI layer
    // ─────────────────────────────────────────────
    public Map<String, Object> explain(CodebaseInfo codebaseInfo) throws IOException, InterruptedException {
        // Build request body: { codebaseJSON: {...}, level: "beginner" }
        Map<String, Object> body = new HashMap<>();
        body.put("codebaseJSON", codebaseInfo);
        body.put("level", codebaseInfo.getLevel() != null ? codebaseInfo.getLevel() : "beginner");

        String jsonBody = objectMapper.writeValueAsString(body);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(aiLayerUrl + "/explain"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        return objectMapper.readValue(response.body(), Map.class);
    }

    // ─────────────────────────────────────────────
    // Call /ask on your Node.js AI layer
    // ─────────────────────────────────────────────
    public Map<String, Object> ask(String question, CodebaseInfo codebaseInfo) throws IOException, InterruptedException {
        Map<String, Object> body = new HashMap<>();
        body.put("question", question);
        body.put("codebaseJSON", codebaseInfo);

        String jsonBody = objectMapper.writeValueAsString(body);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(aiLayerUrl + "/ask"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        return objectMapper.readValue(response.body(), Map.class);
    }
}
