package com.codenav.backend.util;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class RepoParser {

    public static List<String> getAllJavaFiles(String path) {
        List<String> files = new ArrayList<>();
        scan(new File(path), files);
        return files;
    }

    private static void scan(File file, List<String> files) {
        if (file.isDirectory()) {
            File[] fileList = file.listFiles();

            if (fileList != null) {  // 🔥 avoids null crash
                for (File f : fileList) {
                    scan(f, files);
                }
            }
        } else if (file.getName().endsWith(".java")) {
            files.add(file.getAbsolutePath());
        }
    }
}