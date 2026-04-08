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

    // 🔥 ENTRY POINT DETECTION
    public static String findEntryPoint(String path) {
        List<String> files = getAllJavaFiles(path);

        for (String filePath : files) {
            try {
                File file = new File(filePath);
                Scanner scanner = new Scanner(file);

                while (scanner.hasNextLine()) {
                    String line = scanner.nextLine();

                    if (line.contains("@SpringBootApplication") ||
                        line.contains("public static void main")) {

                        scanner.close();
                        return filePath;
                    }
                }

                scanner.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        return "No entry point found";
    }
}