# 🍽️ 급식 알리미

GitHub Actions를 이용해서 매일 오전 7시(KST)에 CJ Freshmeal API를 호출하고, 식단 정보를 Slack Webhook으로 전송하는 자동화 시스템입니다.

## 📁 프로젝트 구조

```
lunch_menu/
├── .github/
│   └── workflows/
│       └── daily_meal.yml       # GitHub Actions 워크플로우
├── send_meal_to_slack.py        # Python 스크립트
├── requirements.txt             # Python 의존성
└── README.md                   # 프로젝트 설명서
```

## 🚀 기능

- **자동 스케줄링**: 매일 오전 7시 KST에 자동 실행
- **CJ Freshmeal API 연동**: 학교 급식 정보 조회
- **Slack 알림**: Webhook을 통한 급식 메뉴 전송
- **에러 처리**: API 호출 실패 시 적절한 에러 메시지
- **로깅**: 실행 과정 추적 및 디버깅

## ⚙️ 설정 방법

### 1. GitHub Secrets 설정

GitHub 리포지토리의 Settings > Secrets and variables > Actions에서 다음 시크릿을 설정하세요:

- `CJ_API_KEY`: CJ Freshmeal API 키
- `SLACK_WEBHOOK_URL`: Slack Webhook URL
- `SCHOOL_CODE`: 학교 코드

### 2. Slack Webhook 설정

1. Slack 워크스페이스에서 앱 생성
2. Incoming Webhooks 활성화
3. Webhook URL 생성 및 복사
4. GitHub Secrets에 `SLACK_WEBHOOK_URL`로 저장

### 3. CJ Freshmeal API 키 발급

1. CJ Freshmeal 개발자 포털에서 API 키 발급
2. 학교 코드 확인
3. GitHub Secrets에 저장

## 📅 실행 스케줄

- **실행 시간**: 매일 오전 7시 KST (UTC 22:00)
- **실행 환경**: GitHub Actions (Ubuntu Latest)
- **수동 실행**: GitHub Actions 탭에서 `workflow_dispatch`로 수동 실행 가능

## 🔧 로컬 테스트

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export CJ_API_KEY="your_api_key"
export SLACK_WEBHOOK_URL="your_webhook_url"
export SCHOOL_CODE="your_school_code"

# 스크립트 실행
python send_meal_to_slack.py
```

## 📊 Slack 메시지 형식

```
🍽️ 12월 25일 (Monday) 급식 메뉴

🌅 아침
• 흰쌀밥
• 미역국
• 계란말이
• 김치

☀️ 점심
• 잡곡밥
• 된장찌개
• 제육볶음
• 시금치나물
• 깍두기

🌙 저녁
• 메뉴 정보 없음

📊 영양 정보
• 칼로리: 850kcal
• 단백질: 35g
• 지방: 25g
```

## 🛠️ 기술 스택

- **Python 3.11**: 메인 스크립트 언어
- **GitHub Actions**: 자동화 및 스케줄링
- **CJ Freshmeal API**: 급식 정보 조회
- **Slack Webhook**: 알림 전송
- **requests**: HTTP 클라이언트
- **python-dotenv**: 환경 변수 관리

## 🔍 문제 해결

### API 호출 실패
- API 키와 학교 코드 확인
- 네트워크 연결 상태 확인
- CJ Freshmeal 서비스 상태 확인

### Slack 전송 실패
- Webhook URL 유효성 확인
- Slack 앱 권한 설정 확인
- 메시지 형식 검증

### 스케줄 실행 안됨
- GitHub Actions 권한 확인
- Secrets 설정 확인
- 워크플로우 파일 문법 검증

## 📝 라이선스

MIT License

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 