# 🛡️ Py-SecScanner & Hardening Pipeline

본 저장소는 Python 기반의 취약점 스캐너와 컨테이너 공급망 보안 하드닝 파이프라인을 포함하고 있습니다.

## 📂 프로젝트 구성

### 1. 🔍 Python Vulnerability Scanner
웹 애플리케이션 및 컨테이너 환경의 취약점을 탐색하는 파이썬 기반 도구입니다.
- **주요 파일**: `src/`, `tests/`, `requirements.txt`
- **상세 설명**: [README_Scanner.md](./README_Scanner.md)

### 2. 🏗️ Container Hardening Pipeline
Java/Spring Boot 애플리케이션을 대상으로 하는 보안 하드닝 파이프라인 실습 환경입니다.
- **주요 폴더**: `vulnerable-spring-app/`
- **상세 설명**: [vulnerable-spring-app/README.md](./vulnerable-spring-app/README.md)

---

## 🛠️ 시작하기

### 스캐너 설치 및 실행
```bash
pip install -r requirements.txt
python src/main.py
```

### 보안 하드닝 파이프라인 확인
`vulnerable-spring-app` 폴더 내의 Dockerfile과 GitHub Actions 설정을 확인하여 보안 하드닝 과정을 학습할 수 있습니다.
