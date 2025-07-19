# PythonAnywhere 배포 가이드

## 1. PythonAnywhere 계정 생성

1. [PythonAnywhere.com](https://www.pythonanywhere.com)에 접속
2. "Create a Beginner account" 클릭 (무료)
3. 사용자명, 이메일, 비밀번호 입력하여 계정 생성

## 2. 파일 업로드

### 방법 1: Git 사용 (권장)
```bash
# 로컬에서 Git 저장소 생성
git init
git add .
git commit -m "Initial commit"

# GitHub에 푸시 (GitHub 계정 필요)
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### 방법 2: 직접 업로드
1. PythonAnywhere 대시보드에서 "Files" 탭 클릭
2. 파일들을 하나씩 업로드

## 3. PythonAnywhere에서 설정

### 3.1 파일 업로드 (Git 사용 시)
```bash
# PythonAnywhere Bash 콘솔에서
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 3.2 가상환경 생성
```bash
# PythonAnywhere Bash 콘솔에서
python3.11 -m venv lca_env
source lca_env/bin/activate
pip install -r requirements.txt
```

### 3.3 WSGI 파일 생성
PythonAnywhere 대시보드에서 "Web" 탭 클릭 후:

1. "Add a new web app" 클릭
2. "Manual configuration" 선택
3. Python 버전 선택 (3.11 권장)
4. "Next" 클릭

### 3.4 WSGI 파일 수정
```python
# /var/www/yourusername_pythonanywhere_com_wsgi.py 파일을 다음과 같이 수정:

import sys
import os

# 프로젝트 디렉토리 추가
path = '/home/yourusername/your-repo-name'
if path not in sys.path:
    sys.path.append(path)

# 환경변수 설정
os.environ['PYTHONPATH'] = path

# 앱 import
from app import app as application

# 서버 객체 설정
server = application.server
```

### 3.5 가상환경 경로 설정
Web 탭에서:
- "Virtual environment" 섹션에서 가상환경 경로 설정:
  `/home/yourusername/your-repo-name/lca_env`

### 3.6 정적 파일 설정
Web 탭에서:
- "Static files" 섹션에서:
  - URL: `/static/`
  - Directory: `/home/yourusername/your-repo-name/static/`

## 4. 앱 실행

1. Web 탭에서 "Reload" 버튼 클릭
2. 웹사이트 URL 확인 (보통 `yourusername.pythonanywhere.com`)

## 5. 문제 해결

### 5.1 로그 확인
Web 탭에서 "Log files" 섹션의 링크들을 클릭하여 오류 로그 확인

### 5.2 일반적인 문제들

**Import 오류:**
```bash
# 가상환경에서 패키지 재설치
source lca_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**경로 오류:**
- WSGI 파일의 경로가 정확한지 확인
- 프로젝트 디렉토리 구조 확인

**포트 오류:**
- PythonAnywhere에서는 포트 8050 대신 내장 웹서버 사용

## 6. 데이터 지속성

PythonAnywhere 무료 계정에서는:
- 파일 시스템이 지속됨
- 세션 데이터는 서버 재시작 시 사라질 수 있음
- 중요한 데이터는 JSON 파일로 저장 권장

## 7. 성능 최적화

1. **디버그 모드 비활성화**: `debug=False`
2. **불필요한 파일 제거**: `.gitignore`에 명시된 파일들
3. **정적 파일 최적화**: CSS/JS 파일 압축

## 8. 보안 고려사항

1. **환경변수**: 민감한 정보는 환경변수로 관리
2. **파일 권한**: 적절한 파일 권한 설정
3. **HTTPS**: PythonAnywhere는 자동으로 HTTPS 제공

## 9. 모니터링

- Web 탭에서 CPU 사용량, 메모리 사용량 확인
- 로그 파일을 통한 오류 모니터링
- 무료 계정 제한사항 확인 (CPU 시간, 저장공간 등) 