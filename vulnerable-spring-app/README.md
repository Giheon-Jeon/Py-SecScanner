# 🛡️ Container Supply Chain Security Hardening Project

본 프로젝트는 컨테이너 기반 공급망 보안을 강화하기 위한 단계별 하드닝 파이프라인을 구축한 사례입니다.

## 🚀 프로젝트 구조
- `vulnerable-spring-app/`: 보안 하드닝 대상 Java/Spring Boot 프로젝트
  - `Dockerfile.vulnerable`: 보안 하드닝 전 (대조군)
  - `Dockerfile.hardened`: 보안 하드닝 후 (개선군)
  - `scripts/`: 보안 자동화 스크립트 모음
    - `scan_parser.py`: 취약점 스캔 결과(JSON) 파싱 및 빌드 제어
    - `check_compliance.py`: Dockerfile 보안 규정 준수 검사
    - `generate_report.py`: 하드닝 결과 분석 보고서 자동 생성
- `.github/workflows/`: 자동화된 보안 파이프라인 (CI/CD)

## 🛠️ 주요 단계별 결과물

### 1단계: 취약한 베이스라인 구축
- 패치되지 않은 베이스 이미지(`ubuntu:18.04`) 및 Root 권한 설정.
- 불필요한 패키지 대거 포함을 통한 공격 표면(Attack Surface) 시뮬레이션.

### 2단계: 자동 진단 체계 구축
- Trivy 스캔 결과를 파이썬 스크립트로 분석하여 **High/Critical** 취약점 발견 시 빌드 차단.

### 3~4단계: 하드닝 및 검증
- **Multi-stage Build** 및 **Distroless** 이미지 적용.
- **Non-root (UID 65532)** 계정 실행.
- 코드 내 하드코딩된 시크릿을 환경 변수로 이전.

### 5단계: 분석 및 보고서 자동화
- 하드닝 전후 지표(취약점 수, 이미지 용량)를 비교하는 HTML 보고서 자동 생성.

## 📖 실행 방법

### 1. 보안 규정 준수 검사 (Compliance Check)
```bash
python vulnerable-spring-app/scripts/check_compliance.py vulnerable-spring-app/Dockerfile.hardened
```

### 2. 하드닝 보고서 생성 (Report Generation)
```bash
python vulnerable-spring-app/scripts/generate_report.py
```

## 📈 보안 개선 기대 효과
- **공격 표면 감소**: 이미지 크기 약 70% 이상 축소 및 불필요 도구 제거.
- **권한 최소화**: Root 권한 제거를 통해 컨테이너 탈취 시 호스트 전이 위험 방지.
- **지속적 보안**: CI 단계에서 자동 스캔을 통한 취약점 라이브러리 유입 원천 차단.
