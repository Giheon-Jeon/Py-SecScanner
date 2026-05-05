import requests
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from concurrent.futures import ThreadPoolExecutor, as_completed
from .payloads import PAYLOADS
from utils.helpers import get_random_user_agent

class ScannerEngine:
    def __init__(self, target_url, max_workers=5):
        self.target_url = target_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": get_random_user_agent()})
        self.results = []
        self.max_workers = max_workers


    def submit_form(self, form_details, url, value):
        # ... (기존 코드와 동일)
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
        except Exception:
            return None

    def scan_url_params(self, url):
        """URL의 쿼리 파라미터를 스캔합니다."""
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        
        if not params:
            return

        print(f"[*] URL 파라미터 분석 중... ({url})")
        for param in params:
            for vulnerability_type, payloads in PAYLOADS.items():
                if vulnerability_type == "ssrf": continue # SSRF는 별도 로직 권장
                
                def check_fn(response, payload):
                    if vulnerability_type == "xss": return payload in response.text
                    if vulnerability_type == "sqli": return any(err in response.text.lower() for err in ["sql syntax", "mysql_fetch_array"])
                    if vulnerability_type == "lfi": return any(pat in response.text for pat in ["root:x:0:0", "bin/bash"])
                    if vulnerability_type == "command_injection": return any(pat in response.text for pat in ["uid=", "root:x:0:0"])
                    return False

                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = []
                    for payload in payloads:
                        # 파라미터 값 교체
                        test_params = params.copy()
                        test_params[param] = [payload]
                        test_url = parsed_url._replace(query=urlencode(test_params, doseq=True)).geturl()
                        futures.append(executor.submit(self.session.get, test_url, timeout=5))
                    
                    for future in as_completed(futures):
                        try:
                            response = future.result()
                            payload = payloads[futures.index(future)] # 정확한 페이로드 매칭을 위해 수정 필요할 수 있음
                            if response and check_fn(response, payload):
                                self.results.append({
                                    "type": f"{vulnerability_type.upper()} (URL Param)",
                                    "url": url,
                                    "payload": payload,
                                    "method": "GET",
                                    "parameter": param
                                })
                                break # 해당 파라미터에서 취약점 발견 시 다음 파라미터로
                        except Exception:
                            continue

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


