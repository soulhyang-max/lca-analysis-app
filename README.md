# LCA (Life Cycle Assessment) 분석 웹 애플리케이션

이 웹 애플리케이션은 생명주기 평가(LCA) 분석을 위한 대시보드입니다.

## 주요 기능

- **투입물 관리**: 원료물질, 보조물질, 에너지, 유틸리티, 수송, 폐기물처리 분류별 투입물 입력
- **DB 목록 관리**: 영향범주 데이터베이스 관리
- **LCA 분석**: 25개 영향범주에 대한 자동 계산 및 결과 표시
- **데이터 지속성**: 세션 기반 데이터 저장

## 영향범주 (25개)

1. acidification (mol H+-Eq)
2. climate change: biogenic (kg CO2-Eq)
3. climate change: fossil (kg CO2-Eq)
4. climate change: land use and land use change (kg CO2-Eq)
5. climate change (kg CO2-Eq)
6. ecotoxicity: freshwater, inorganics (CTUe)
7. ecotoxicity: freshwater, organics (CTUe)
8. ecotoxicity: freshwater (CTUe)
9. energy resources: non-renewable (MJ, net calorific value)
10. eutrophication: freshwater (kg P-Eq)
11. eutrophication: marine (kg N-Eq)
12. eutrophication: terrestrial (mol N-Eq)
13. human toxicity: carcinogenic, inorganics (CTUh)
14. human toxicity: carcinogenic, organics (CTUh)
15. human toxicity: carcinogenic (CTUh)
16. human toxicity: non-carcinogenic, inorganics (CTUh)
17. human toxicity: non-carcinogenic, organics (CTUh)
18. human toxicity: non-carcinogenic (CTUh)
19. ionising radiation: human health (kBq U235-Eq)
20. land use (dimensionless)
21. material resources: metals/minerals (kg Sb-Eq)
22. ozone depletion (kg CFC-11-Eq)
23. particulate matter formation (disease incidence)
24. photochemical oxidant formation: human health (kg NMVOC-Eq)
25. water use (m3 world Eq deprived)

## 사용법

1. **투입물 입력**: 투입물 메뉴에서 물질명, 투입량, 분류, DB명, 국가 등을 입력
2. **DB 검색**: 연결 DB 검색 버튼을 통해 사용 가능한 DB 목록에서 선택
3. **LCA 분석**: LCA 분석결과 메뉴에서 "LCA 분석 실행" 버튼 클릭
4. **결과 확인**: 25개 영향범주별 결과값을 지수 형태로 확인

## 기술 스택

- **Frontend**: Dash, Dash Bootstrap Components
- **Backend**: Python, Flask
- **Data Processing**: Pandas, NumPy
- **Deployment**: Heroku, Gunicorn

## 로컬 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 패키지 설치
pip install -r requirements.txt

# 앱 실행
python app.py
```

## PythonAnywhere 배포

자세한 배포 가이드는 `PYTHONANYWHERE_DEPLOYMENT.md` 파일을 참조하세요.

### 간단한 배포 단계:

1. **PythonAnywhere 계정 생성**: [pythonanywhere.com](https://www.pythonanywhere.com)
2. **GitHub에 코드 업로드**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```
3. **PythonAnywhere에서 Git 클론**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   ```
4. **가상환경 생성 및 패키지 설치**:
   ```bash
   python3.11 -m venv lca_env
   source lca_env/bin/activate
   pip install -r requirements.txt
   ```
5. **웹앱 설정**: PythonAnywhere 대시보드에서 Web 탭에서 설정
6. **WSGI 파일 수정**: 배포 가이드 참조
7. **앱 실행**: Reload 버튼 클릭

### 무료 계정 제한사항:
- CPU 시간: 월 1000초
- 저장공간: 512MB
- 웹사이트: 1개
- 커스텀 도메인: 불가 