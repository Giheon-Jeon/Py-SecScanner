import sys
from scanner.crawler import Crawler
from scanner.engine import ScannerEngine
from scanner.reporter import Reporter
from scanner.fuzzer import Fuzzer
from scanner.headers import HeaderAnalyzer

def main():
    if len(sys.argv) < 2:
        print("사용법: python main.py <Target_URL>")
        print("예: python main.py http://example.com")
        sys.exit(1)

    target_url = sys.argv[1]
    print(f"\n[*] '{target_url}'에 대한 취약점 스캔을 시작합니다...")

    # 1. 보안 헤더 분석
    header_analyzer = HeaderAnalyzer(target_url)
    header_results = header_analyzer.analyze()

    # 2. 크롤링 (폼 발견)
    crawler = Crawler(target_url)
    forms = crawler.get_forms()
    print(f"[+] 발견된 폼 개수: {len(forms)}")

    # 3. 스캔 수행
    engine = ScannerEngine(target_url)
    reporter = Reporter()

    for form in forms:
        form_details = crawler.extract_form_details(form)
        print(f"[*] 폼 분석 중... (Action: {form_details['action']}, Method: {form_details['method']})")
        
        # XSS 스캔
        if engine.scan_xss(form_details):
            print("[!] XSS 취약점 발견!")
        
        # SQLi 스캔
        if engine.scan_sqli(form_details):
            print("[!] SQL Injection 취약점 발견!")

        # LFI 스캔
        if engine.scan_lfi(form_details):
            print("[!] LFI 취약점 발견!")

        # Command Injection 스캔
        if engine.scan_command_injection(form_details):
            print("[!] Command Injection 취약점 발견!")

    # 4. 퍼징 (디렉토리 탐색)
    fuzzer = Fuzzer(target_url)
    fuzz_results = fuzzer.run()

    # 5. 결과 리포트
    for res in engine.results:
        reporter.add_result(res)
    
    reporter.generate_report(fuzzing_results=fuzz_results, header_results=header_results)


if __name__ == "__main__":
    main()


