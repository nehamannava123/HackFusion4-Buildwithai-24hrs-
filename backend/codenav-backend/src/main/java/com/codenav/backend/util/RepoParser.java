package com.codenav.backend.util;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class RepoParser {

    // 🔹 Get all Java files
    public static List<String> getAllJavaFiles(String path) {
        List<String> files = new ArrayList<>();
        scan(new File(path), files);
        return files;
    }

    private static void scan(File file, List<String> files) {
        if (file == null || !file.exists()) return;

        if (file.isDirectory()) {
            for (File f : file.listFiles()) {
                scan(f, files);
            }
        } else if (file.getName().endsWith(".java")) {
            files.add(file.getAbsolutePath());
        }
    }

    // 🔹 Find entry point (main class)
    public static List<String> findEntryPoint(String path) {
        List<String> files = getAllJavaFiles(path);
        List<String> entryPoints = new ArrayList<>();

        for (String file : files) {
            if (file.contains("Application.java")) {
                entryPoints.add(file);
            }
        }

        return entryPoints;
    }

    // 🔹 Detect Controller → Service → Repository flow
    public static List<String> findControllerServiceFlow(String path) {
        List<String> files = getAllJavaFiles(path);
        List<String> flow = new ArrayList<>();

        for (String file : files) {
            if (file.toLowerCase().contains("controller")) {
                flow.add("Controller → " + file);
            } else if (file.toLowerCase().contains("service")) {
                flow.add("Service → " + file);
            } else if (file.toLowerCase().contains("repository")) {
                flow.add("Repository → " + file);
            }
        }

        return flow;
    }
}