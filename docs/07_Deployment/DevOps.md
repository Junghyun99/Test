# DevOps Documentation

이 문서는 자동 주식 매매 시스템의 DevOps 전략, 도구, 및 운영 전반의 정책을 설명합니다. 본 시스템은 Python 기반 자동 매매 엔진, sqlite3 데이터베이스, 그리고 GitHub Actions와 GitHub Pages를 활용한 배포 및 스케줄링 환경으로 구축되어 있습니다.

---

## 1. 버전 관리 & 브랜칭 전략

- **버전 관리 도구:**  
  - GitHub를 사용합니다.
- **브랜칭 전략:**  
  - **main:** 안정적인 릴리즈 버전 유지  
  - **develop:** 개발된 기능들이 통합되는 브랜치  
  - **feature/**, **hotfix/** 브랜치를 사용하여 기능 개발 및 버그 수정을 진행하며, 코드 리뷰 후 develop 또는 main으로 병합

---

## 2. Continuous Integration (CI)

- **도구:**  
  - GitHub Actions
- **주요 기능:**  
  - 코드 커밋 시 자동으로 유닛 테스트, 정적 코드 분석, 린팅 등을 실행하여 코드 품질을 보증
- **프로세스:**  
  - 코드 push 후 GitHub Actions가 트리거되어 빌드 및 테스트 수행  
  - 모든 테스트가 통과할 때에만 다음 단계(배포) 진행

---

## 3. Continuous Deployment (CD)

- **배포 도구:**  
  - GitHub Actions 및 GitHub Pages 활용
- **배포 환경:**  
  - **모바일 UI:** GitHub Pages를 통해 정적 웹 자산으로 배포  
  - **자동 매매 스크립트:** GitHub Actions의 Cron 스케줄러를 통해 주기적 실행 (예: 매 5분 실행)
- **환경 변수/Secrets 관리:**  
  - 증권사 API KEY 등 민감 정보는 GitHub Repository의 Secrets에 암호화하여 저장

---

## 4. 빌드 및 배포 프로세스

1. **빌드 단계**
   - GitHub Actions 워크플로우가 Python 프로젝트를 빌드하고, 필요한 라이브러리를 설치합니다.
   - 예: `pip install -r requirements.txt`
  
2. **테스트 단계**
   - 단위 테스트와 통합 테스트가 실행됩니다.
   - 모든 테스트를 통과해야 다음 단계로 진행합니다.
  
3. **배포 단계**
   - **모바일 UI 배포:**  
     - 정적 HTML, CSS, JavaScript 파일을 GitHub Pages에 배포합니다.
   - **자동 매매 스크립트 실행:**  
     - GitHub Actions의 Cron 스케줄러를 통해 정기적으로 Python 스크립트를 실행하여, 매매 조건 체크 및 주문 실행을 수행합니다.
   - 배포 후, 성공/실패 로그는 GitHub Actions 로그에 기록되고, 필요 시 Slack 또는 이메일 알림을 통해 통보합니다.

---

## 5. 모니터링 및 로그 관리

- **로그 기록:**  
  - Python의 `logging` 모듈을 활용하여 애플리케이션 로그 기록
  - GitHub Actions의 실행 로그를 통해 배포 및 작업 상태 모니터링
- **모니터링 도구:**  
  - GitHub Actions 로그, 필요 시 추가적인 외부 모니터링(예: Sentry, Prometheus 등) 도입 고려 가능

---

## 6. 롤백 및 장애 복구

- **롤백 전략:**  
  - 배포 실패 시 이전 안정 버전으로 자동 롤백하는 GitHub Actions 스크립트를 구성
  - 주요 배포 후 이상 징후 감지 시, GitHub 내에서 Revert Commit을 통해 빠른 롤백 수행
- **장애 복구:**  
  - 배포된 시스템은 장애 발생 시, GitHub Actions 로그를 분석하여 문제점을 파악하고, 즉시 수정
  - 너무 잦은 실패 시, 수동 개입과 재배포 절차를 마련

---

## 7. Workflow Diagram (ASCII 예시)
[Developer] ---> [GitHub Repository (Push Code)] 
│ 
▼ 
[GitHub Actions CI Pipeline] 
│   (Test, Lint, Build) 
▼ 
[Passing Build?] ---- No ----- [Notify & Fail Build] 
│ Yes 
│ 
▼ 
[GitHub Actions CD Pipeline] 
│ 
├--> [Deploy UI to GitHub Pages] 
│ └--> [Schedule Cron Job for Trading Script] 
│         (정기적 실행: 매 5분) 
▼ 
[Monitoring & Logging (GitHub Actions Logs)]


---

## 8. 미래 개선 방안

- **컨테이너화:**  
  - 향후 확장성을 고려하여 Docker를 통한 컨테이너화 도입 검토
- **고급 모니터링 도입:**  
  - Sentry, Prometheus 등 통합 모니터링 도구 도입 고려
- **자동화 개선:**  
  - 배포 시 Blue-Green 배포 등 무중단 배포 기법 도입 검토

---

이 DevOps.md 문서는 자동 주식 매매 시스템의 개발부터 배포, 운영까지의 전체 라이프사이클을 지원하기 위한 가이드라인으로, 현재 개인 프로젝트 환경에 맞추어 구성되었습니다. 필요에 따라 단계별 프로세스와 도구를 업데이트하면서 지속적으로 개선할 수 있습니다.