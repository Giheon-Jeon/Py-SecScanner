import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()

    def get_forms(self):
        """대상 URL에서 모든 폼을 찾아 반환합니다."""
        try:
            response = self.session.get(self.target_url)
            soup = BeautifulSoup(response.content, "html.parser")
            return soup.find_all("form")
        except Exception as e:
            print(f"[-] Crawling error: {e}")
            return []

    def extract_form_details(self, form):
        """폼의 상세 정보(action, method, inputs)를 추출합니다."""
        details = {}
        action = form.attrs.get("action")
        method = form.attrs.get("method", "get").lower()
        inputs = []
        
        for input_tag in form.find_all(["input", "textarea", "select"]):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            inputs.append({"type": input_type, "name": input_name})
            
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details

