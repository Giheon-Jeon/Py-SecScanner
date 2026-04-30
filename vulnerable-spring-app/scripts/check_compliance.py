import re
import sys
import os

def check_dockerfile_compliance(file_path):
    """
    Dockerfile의 보안 설정을 검증합니다.
    """
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return False

    violations = []
    has_user_non_root = False
    
    with open(file_path, 'r') as f:
        content = f.read()
        lines = content.splitlines()

    for i, line in enumerate(lines):
        # 1. USER root 검사
        if re.search(r'^\s*USER\s+root', line, re.IGNORECASE):
            violations.append(f"Line {i+1}: Critical security risk - 'USER root' detected.")
        
        # 2. Non-root USER 설정 확인
        if re.search(r'^\s*USER\s+(?!root)\S+', line, re.IGNORECASE):
            has_user_non_root = True

        # 3. 최신 이미지가 아닌 태그 사용 검사 (예: latest 금지)
        if re.search(r'^\s*FROM\s+\S+:latest', line, re.IGNORECASE):
            violations.append(f"Line {i+1}: Warning - Using ':latest' tag can lead to unpredictable builds.")

    # 4. USER 설정 누락 검사
    if not has_user_non_root:
        violations.append("Global: No non-root USER defined. Container will run as root by default.")

    if violations:
        print(f"\n[!] Compliance Check Failed for {file_path}:")
        for v in violations:
            print(f"  - {v}")
        return False
    
    print(f"\n[+] Compliance Check Passed for {file_path}. Best practices followed.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_compliance.py <dockerfile_path>")
        sys.exit(1)
        
    target_dockerfile = sys.argv[1]
    success = check_dockerfile_compliance(target_dockerfile)
    
    if not success:
        sys.exit(1)
    sys.exit(0)
