import json
import sys
import argparse

def parse_trivy_report(file_path, fail_on_severity=['CRITICAL', 'HIGH']):
    """
    Trivy JSON 보고서를 파싱하여 특정 수준 이상의 취약점이 있는지 확인합니다.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Report file {file_path} not found.")
        return False
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
        return False

    vulnerabilities_found = []
    
    # Trivy JSON 구조 탐색 (Results 키 아래에 취약점 정보가 있음)
    results = data.get('Results', [])
    for result in results:
        vulnerabilities = result.get('Vulnerabilities', [])
        for vuln in vulnerabilities:
            severity = vuln.get('Severity')
            if severity in fail_on_severity:
                vulnerabilities_found.append({
                    'ID': vuln.get('VulnerabilityID'),
                    'Package': vuln.get('PkgName'),
                    'Severity': severity,
                    'FixedVersion': vuln.get('FixedVersion', 'N/A')
                })

    if vulnerabilities_found:
        print(f"\n[!] Security Check Failed: Found {len(vulnerabilities_found)} vulnerabilities with severity {fail_on_severity}")
        print("-" * 60)
        for v in vulnerabilities_found[:10]: # 최대 10개만 출력
            print(f"- {v['ID']} | {v['Package']} | {v['Severity']} | Fixed: {v['FixedVersion']}")
        if len(vulnerabilities_found) > 10:
            print(f"... and {len(vulnerabilities_found) - 10} more.")
        return False
    
    print("\n[+] Security Check Passed: No High/Critical vulnerabilities found.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Container Security Scan Parser")
    parser.add_argument("--file", required=True, help="Path to Trivy JSON report")
    parser.add_argument("--fail-high", action="store_true", help="Fail if High severity is found")
    
    args = parser.parse_args()
    
    severities = ['CRITICAL']
    if args.fail_high:
        severities.append('HIGH')
        
    success = parse_trivy_report(args.file, severities)
    
    if not success:
        sys.exit(1) # 빌드 실패 유도
    sys.exit(0)
