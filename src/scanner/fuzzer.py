import requests
from urllib.parse import urljoin

class Fuzzer:
    def __init__(self, target_url):
        self.target_url = target_url
        self.common_paths = [
            "admin/", "login/", "config.php", ".env", ".git/",
            "phpinfo.php", "robots.txt", "backup/", "db/", "api/"
        ]
        self.found_paths = []

    def run(self):
        """일반적인 경로들을 탐색하여 숨겨진 디렉토리나 파일을 찾습니다."""
        print(f"\n[*] 디렉토리 및 파일 퍼징 시작...")
        for path in self.common_paths:
            url = urljoin(self.target_url, path)
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"[+] 발견: {url} (Status: 200)")
                    self.found_paths.append({"url": url, "status": response.status_code})
                elif response.status_code == 403:
                    print(f"[!] 권한 제한: {url} (Status: 403)")
                    self.found_paths.append({"url": url, "status": response.status_code})
            except Exception:
                continue
        return self.found_paths
