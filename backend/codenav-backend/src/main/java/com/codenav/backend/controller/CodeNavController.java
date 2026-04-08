package com.codenav.backend.controller;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class CodeNavController {

    @GetMapping("/test")
    public String test() {
        return "Backend is working ";
    }
}