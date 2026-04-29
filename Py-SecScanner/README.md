# Py-SecScanner

파이썬 기반 웹 취약점 스캐너 프로젝트입니다.

## 프로젝트 구조

```
Py-SecScanner/
├── .github/              # PR 템플릿 등 설정
├── src/                  # 소스 코드 메인
│   ├── main.py           # 실행 엔트리 포인트
│   ├── scanner/          # 스캔 로직 모듈
│   │   ├── crawler.py    # URL 수집기
│   │   ├── payloads.py   # 취약점 테스트 페이로드
│   │   └── reporter.py   # 결과 리포트 생성
│   └── utils/            # 공통 유틸리티
├── tests/                # 유닛 테스트 코드
├── requirements.txt      # 의존성 목록
└── README.md             # 프로젝트 설명
```
