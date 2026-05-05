import requests

class HeaderAnalyzer:
    def __init__(self, target_url):
        self.target_url = target_url
        self.missing_headers = []
        self.security_headers = [
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Strict-Transport-Security",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

    def analyze(self):
        """대상 URL의 응답 헤더를 분석하여 누락된 보안 헤더를 찾습니다."""
        print(f"\n[*] 보안 헤더 분석 시작: {self.target_url}")
        try:
            response = requests.get(self.target_url, timeout=5)
            headers = response.headers
            
            for header in self.security_headers:
                if header not in headers:
                    self.missing_headers.append(header)
            
            return self.missing_headers
        except Exception as e:
            print(f"[-] 헤더 분석 중 오류 발생: {e}")
            return []
