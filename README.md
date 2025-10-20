# SE 지시사항 대시보드 (Streamlit)
이 앱은 `/data/todo.xlsx`(사장 지시사항 관리대장) 기반으로 진행상황을 한눈에 보여줍니다.

## 실행 방법
```bash
pip install streamlit pandas numpy plotly openpyxl python-dateutil
streamlit run app.py
```
(로컬에서 `data/todo.xlsx`를 최신 파일로 교체하세요.)

## 파일 구조
```
app.py
pages/
  1_Overview.py
  2_Department.py
  3_Timeline.py
components/
  kpi_cards.py
  charts.py
  tables.py
utils/
  loader.py
  metrics.py
data/
  todo.xlsx   # 예시/운영 파일
```


---

## 배포(파이썬 미설치 사용자용)

### 1) Streamlit Community Cloud (가장 쉬움)
1. 이 폴더를 GitHub에 푸시
2. https://share.streamlit.io 로그인 → 'New app' → 레포/브랜치/`app.py` 선택 → Deploy
3. 배포된 URL을 공유하면 누구나 브라우저에서 사용 가능

### 2) Hugging Face Spaces (무료 호스팅)
1. Hugging Face 가입 → 'Create Space' → Template: **Streamlit**
2. 이 폴더 파일 업로드(또는 Git push) → 자동 빌드 후 URL 발급

### 3) Docker로 사내 서버/클라우드에 배포
```bash
docker build -t se-todo-dashboard .
docker run -p 8501:8501 -e PORT=8501 se-todo-dashboard
```
→ 브라우저에서 http://서버IP:8501 접속

### 4) (선택) Windows 실행파일 느낌으로 배포
- `run.bat` 더블클릭 → 가상환경 생성/설치/실행 자동화
- 완전한 단일 exe는 권장하지 않음(웹서버 특성상 포트/방화벽 설정 필요)

