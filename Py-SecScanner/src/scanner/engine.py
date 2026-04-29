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
        """SQL Injection 취약점을 스캔합니다."""
        for payload in PAYLOADS["sqli"]:
            response = self.submit_form(form_details, self.target_url, payload)
            if response and any(error in response.text.lower() for error in ["sql syntax", "mysql_fetch_array", "sqlite3.error"]):
                self.results.append({
                    "type": "SQLi",
                    "url": self.target_url,
                    "payload": payload,
                    "method": form_details["method"]
                })
                return True
        return False

    def scan_lfi(self, form_details):
        """Local File Inclusion (LFI) 취약점을 스캔합니다."""
        for payload in PAYLOADS["lfi"]:
            response = self.submit_form(form_details, self.target_url, payload)
            if response and any(pattern in response.text for pattern in ["root:x:0:0", "[extensions]", "bin/bash"]):
                self.results.append({
                    "type": "LFI",
                    "url": self.target_url,
                    "payload": payload,
                    "method": form_details["method"]
                })
                return True
        return False

    def scan_command_injection(self, form_details):
        """Command Injection 취약점을 스캔합니다."""
        for payload in PAYLOADS["command_injection"]:
            response = self.submit_form(form_details, self.target_url, payload)
            if response and any(pattern in response.text for pattern in ["uid=", "groups=", "root:x:0:0"]):
                self.results.append({
                    "type": "Command Injection",
                    "url": self.target_url,
                    "payload": payload,
                    "method": form_details["method"]
                })
                return True
        return False

