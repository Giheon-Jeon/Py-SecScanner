class Reporter:
    def __init__(self):
        self.results = []

    def add_result(self, result):
        """취약점 발견 결과를 리스트에 추가합니다."""
        self.results.append(result)

    def generate_report(self, fuzzing_results=None, header_results=None):
        """최종 리포트를 출력합니다."""
        print("\n" + "="*50)
        print("          취약점 스캔 결과 리포트")
        print("="*50)
        
        # 1. 보안 헤더 분석 결과
        if header_results:
            print("\n[!] 누락된 보안 헤더:")
            for header in header_results:
                print(f"    - {header}")
            print("-" * 30)

        # 2. 폼 취약점 결과
        if not self.results:
            print("\n[+] 발견된 폼 취약점이 없습니다.")
        else:
            print(f"\n[!] 총 {len(self.results)}개의 폼 취약점이 발견되었습니다.\n")
            for i, res in enumerate(self.results, 1):
                print(f"[{i}] 유형: {res['type']}")
                print(f"    - 대상 URL: {res['url']}")
                print(f"    - 페이로드: {res['payload']}")
                print(f"    - 전송 방식: {res['method']}")
                print("-" * 30)

        # 3. 퍼징 결과
        if fuzzing_results:
            print("\n[+] 탐색된 중요 경로:")
            for res in fuzzing_results:
                print(f"    - {res['url']} (Status: {res['status']})")
        
        print("\n" + "="*50 + "\n")



