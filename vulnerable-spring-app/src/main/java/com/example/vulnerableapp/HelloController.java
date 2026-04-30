package com.example.vulnerableapp;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class HelloController {
    private static final Logger logger = LoggerFactory.getLogger(HelloController.class);

    @GetMapping("/")
    public String index() {
        // 보안 하드닝: 하드코딩된 키 대신 환경 변수나 Vault에서 정보를 가져오도록 수정
        String apiKey = System.getenv("APP_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            apiKey = "NOT_SET (Secure Default)";
        }
        
        logger.info("Hello World request received with API Key: {}", apiKey.substring(0, Math.min(apiKey.length(), 4)) + "****");
        return "Hardened App is running! API Key status: " + (apiKey.equals("NOT_SET (Secure Default)") ? "Protected" : "Configured");
    }
}
