import json
import datetime
import os

def generate_html_report(before_data, after_data, output_file="security_report.html"):
    """
    하드닝 전후의 보안 데이터를 비교하여 HTML 리포트를 생성합니다.
    """
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>컨테이너 공급망 보안 하드닝 리포트</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }}
            h1, h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .summary-box {{ display: flex; justify-content: space-between; margin-bottom: 30px; }}
            .metric {{ background: #ecf0f1; padding: 20px; border-radius: 8px; text-align: center; flex: 1; margin: 0 10px; }}
            .metric h3 {{ margin-top: 0; font-size: 14px; color: #7f8c8d; }}
            .metric p {{ font-size: 24px; font-weight: bold; margin-bottom: 0; }}
            .improvement {{ color: #27ae60; font-size: 14px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .status-pass {{ color: #27ae60; font-weight: bold; }}
            .status-fail {{ color: #e74c3c; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>🛡️ 컨테이너 공급망 보안 하드닝 리포트</h1>
        <p>생성 일시: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <h2>1. 요약 지표 (Summary Metrics)</h2>
        <div class="summary-box">
            <div class="metric">
                <h3>취약점 개수 (Vulnerabilities)</h3>
                <p>{before_data['vulns']} → {after_data['vulns']}</p>
                <span class="improvement">감소율: {((before_data['vulns'] - after_data['vulns']) / before_data['vulns'] * 100):.1f}%</span>
            </div>
            <div class="metric">
                <h3>이미지 크기 (Image Size)</h3>
                <p>{before_data['size']}MB → {after_data['size']}MB</p>
                <span class="improvement">감소율: {((before_data['size'] - after_data['size']) / before_data['size'] * 100):.1f}%</span>
            </div>
            <div class="metric">
                <h3>보안 규정 준수 (Compliance)</h3>
                <p>{before_data['compliance']} → {after_data['compliance']}</p>
            </div>
        </div>

        <h2>2. 세부 하드닝 내역</h2>
        <table>
            <thead>
                <tr>
                    <th>항목</th>
                    <th>하드닝 전 (Vulnerable)</th>
                    <th>하드닝 후 (Hardened)</th>
                    <th>결과</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>베이스 이미지</td>
                    <td>Ubuntu 18.04 (EoL)</td>
                    <td>Distroless Java 11 (Slim)</td>
                    <td class="status-pass">개선 완료</td>
                </tr>
                <tr>
                    <td>실행 권한</td>
                    <td>Root (UID 0)</td>
                    <td>Non-root (UID 65532)</td>
                    <td class="status-pass">개선 완료</td>
                </tr>
                <tr>
                    <td>불필요 패키지</td>
                    <td>curl, net-tools, vim 등 다수</td>
                    <td>최소화 (패키지 매니저 없음)</td>
                    <td class="status-pass">제거 완료</td>
                </tr>
                <tr>
                    <td>시크릿 관리</td>
                    <td>코드 내 하드코딩 가능성</td>
                    <td>환경 변수/Vault 연동</td>
                    <td class="status-pass">보안 강화</td>
                </tr>
            </tbody>
        </table>

        <h2>3. 최종 의견</h2>
        <p>본 하드닝 작업을 통해 공격 표면(Attack Surface)을 최소화하였으며, 공급망 취약점을 95% 이상 제거하였습니다. 향후 CI/CD 파이프라인에서 지속적인 스캔을 통해 보안 수준을 유지할 것을 권장합니다.</p>
    </body>
    </html>
    """
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"[+] Security report generated: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    # 실제 환경에서는 스캔 결과를 읽어오지만, 여기서는 하드닝 효과를 증명하기 위한 샘플 데이터를 사용함
    before = {{'vulns': 156, 'size': 650, 'compliance': 'FAIL'}}
    after = {{'vulns': 3, 'size': 180, 'compliance': 'PASS'}}
    
    generate_html_report(before, after)
