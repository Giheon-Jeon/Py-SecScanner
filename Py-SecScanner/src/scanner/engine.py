import requests
from urllib.parse import urljoin
from .payloads import PAYLOADS

class ScannerEngine:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.results = []

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
                return self.session.post(target_url, data=data)
            else:
                return self.session.get(target_url, params=data)
        except Exception as e:
            print(f"[-] Request error: {e}")
            return None

    def scan_xss(self, form_details):
        """XSS 취약점을 스캔합니다."""
        for payload in PAYLOADS["xss"]:
            response = self.submit_form(form_details, self.target_url, payload)
            if response and payload in response.text:
                self.results.append({
                    "type": "XSS",
                    "url": self.target_url,
                    "payload": payload,
                    "method": form_details["method"]
                })
                return True
        return False

    def scan_sqli(self, form_details):
        """SQL Injection 취약점을 스캔합니다. (간단한 응답 변화 체크)"""
        for payload in PAYLOADS["sqli"]:
            response = self.submit_form(form_details, self.target_url, payload)
            # 여기서는 단순히 에러 메시지나 특정 패턴을 체크하는 로직을 추가할 수 있습니다.
            if response and any(error in response.text.lower() for error in ["sql syntax", "mysql_fetch_array", "sqlite3.error"]):
                self.results.append({
                    "type": "SQLi",
                    "url": self.target_url,
                    "payload": payload,
                    "method": form_details["method"]
                })
                return True
        return False
