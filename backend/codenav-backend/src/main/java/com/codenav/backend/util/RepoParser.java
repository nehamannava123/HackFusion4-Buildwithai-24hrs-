package com.codenav.backend.util;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

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
            File[] fileList = file.listFiles();
            if (fileList != null) {
                for (File f : fileList) {
                    scan(f, files);
                }
            }
        } else if (file.getName().endsWith(".java")) {
            files.add(file.getAbsolutePath());
        }
    }

    // 🔹 Entry Point Detection
    public static List<String> findEntryPoint(String path) {
        List<String> files = getAllJavaFiles(path);
        List<String> entryPoints = new ArrayList<>();

        for (String filePath : files) {
            try {
                File file = new File(filePath);
                Scanner scanner = new Scanner(file);

                while (scanner.hasNextLine()) {
                    String line = scanner.nextLine();

                    if (line.contains("@SpringBootApplication") ||
                        line.contains("public static void main")) {

                        entryPoints.add(filePath);
                        break;
                    }
                }

                scanner.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        return entryPoints;
    }

    // 🔹 Flow Detection
    public static List<String> findControllerServiceFlow(String path) {
        List<String> files = getAllJavaFiles(path);
        List<String> flow = new ArrayList<>();

        for (String file : files) {
            String lower = file.toLowerCase();

            if (lower.contains("controller")) {
                flow.add("Controller → " + file);
            } else if (lower.contains("service")) {
                flow.add("Service → " + file);
            } else if (lower.contains("repository")) {
                flow.add("Repository → " + file);
            }
        }

        return flow;
    }
}