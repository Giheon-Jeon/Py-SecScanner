import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from .payloads import PAYLOADS

class ScannerEngine:
    def __init__(self, target_url, max_workers=5):
        self.target_url = target_url
        self.session = requests.Session()
        self.results = []
        self.max_workers = max_workers

    def submit_form(self, form_details, url, value):
        """페이로드를 포함하여 폼을 전송합니다."""
        target_url = urljoin(url, form_details["action"])
        inputs = form_details["inputs"]
        data = {}
        
        for input_field in inputs:
            if input_field["type"] == "text" or input_field["type"] == "search":
                data[input_field["name"]] = value
            else:
                data[input_field["name"]] = "test"
        
        try:
            if form_details["method"] == "post":
                return self.session.post(target_url, data=data, timeout=5)
            else:
                return self.session.get(target_url, params=data, timeout=5)
        except Exception as e:
            # 병렬 실행 중 에러 메시지가 너무 많이 출력되지 않도록 로그 수준 조절 가능
            return None

    def _run_parallel_scan(self, form_details, payloads, check_fn, vulnerability_type):
        """페이로드들을 병렬로 실행하고 취약점을 탐지합니다."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_payload = {
                executor.submit(self.submit_form, form_details, self.target_url, payload): payload 
                for payload in payloads
            }
            
            for future in as_completed(future_to_payload):
                payload = future_to_payload[future]
                try:
                    response = future.result()
                    if response and check_fn(response, payload):
                        result = {
                            "type": vulnerability_type,
                            "url": self.target_url,
                            "payload": payload,
                            "method": form_details["method"]
                        }
                        self.results.append(result)
                        return True
                except Exception:
                    continue
        return False

    def scan_xss(self, form_details):
        """XSS 취약점을 병렬로 스캔합니다."""
        def check_xss(response, payload):
            return payload in response.text
            
        return self._run_parallel_scan(form_details, PAYLOADS["xss"], check_xss, "XSS")

    def scan_sqli(self, form_details):
        """SQL Injection 취약점을 병렬로 스캔합니다."""
        def check_sqli(response, payload):
            errors = ["sql syntax", "mysql_fetch_array", "sqlite3.error", "oracle error", "postgresql error"]
            return any(error in response.text.lower() for error in errors)
            
        return self._run_parallel_scan(form_details, PAYLOADS["sqli"], check_sqli, "SQLi")

    def scan_lfi(self, form_details):
        """Local File Inclusion (LFI) 취약점을 병렬로 스캔합니다."""
        def check_lfi(response, payload):
            patterns = ["root:x:0:0", "[extensions]", "bin/bash", "boot loader"]
            return any(pattern in response.text for pattern in patterns)
            
        return self._run_parallel_scan(form_details, PAYLOADS["lfi"], check_lfi, "LFI")

    def scan_command_injection(self, form_details):
        """Command Injection 취약점을 병렬로 스캔합니다."""
        def check_cmd(response, payload):
            patterns = ["uid=", "groups=", "root:x:0:0", "Windows IP Configuration"]
            return any(pattern in response.text for pattern in patterns)
            
        return self._run_parallel_scan(form_details, PAYLOADS["command_injection"], check_cmd, "Command Injection")


