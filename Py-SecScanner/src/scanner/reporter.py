class Reporter:
    def __init__(self):
        self.results = []

    def add_result(self, result):
        """취약점 발견 결과를 리스트에 추가합니다."""
        self.results.append(result)

    def generate_report(self):
        """최종 리포트를 출력합니다."""
        print("\n" + "="*50)
        print("          취약점 스캔 결과 리포트")
        print("="*50)
        
        if not self.results:
            print("[+] 발견된 취약점이 없습니다. 안전해 보입니다!")
        else:
            print(f"[!] 총 {len(self.results)}개의 취약점이 발견되었습니다.\n")
            for i, res in enumerate(self.results, 1):
                print(f"[{i}] 유형: {res['type']}")
                print(f"    - 대상 URL: {res['url']}")
                print(f"    - 페이로드: {res['payload']}")
                print(f"    - 전송 방식: {res['method']}")
                print("-" * 30)
        
        print("="*50 + "\n")

