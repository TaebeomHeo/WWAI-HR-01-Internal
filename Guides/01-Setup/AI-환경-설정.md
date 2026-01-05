# AI 환경 설정 가이드

이 가이드는 AI를 활용해 자연어로 데이터베이스를 조회하는 환경을 설정하는 방법을 안내합니다.

## 목차
1. [Visual Studio Code 설치](#1-visual-studio-code-설치)
2. [Python 설치](#2-python-설치)
3. [Node.js 설치](#3-nodejs-설치)
4. [Claude Code Extension 설치](#4-claude-code-extension-설치)
5. [프로젝트 클론 및 설정](#5-프로젝트-클론-및-설정)
6. [AI로 자연어 조회하기](#6-ai로-자연어-조회하기)

---

## 1. Visual Studio Code 설치

### 다운로드
1. [VS Code 공식 웹사이트](https://code.visualstudio.com/) 접속
2. 운영체제에 맞는 버전 다운로드
   - **macOS**: `.dmg` 파일 다운로드
   - **Windows**: `.exe` 설치 파일 다운로드

### 설치
- **macOS**:
  1. 다운로드한 `.dmg` 파일 실행
  2. VS Code 아이콘을 Applications 폴더로 드래그
  3. Applications에서 VS Code 실행

- **Windows**:
  1. 다운로드한 설치 파일 실행
  2. 설치 마법사 따라 진행
  3. "PATH에 추가" 옵션 선택 권장

### 확인
```bash
code --version
```

---

## 2. Python 설치

### 다운로드 및 설치

**macOS**:
```bash
# Homebrew를 통한 설치 (권장)
brew install python3

# 또는 공식 웹사이트에서 다운로드
# https://www.python.org/downloads/
```

**Windows**:
1. [Python 공식 웹사이트](https://www.python.org/downloads/) 접속
2. 최신 Python 3.x 버전 다운로드
3. 설치 시 **"Add Python to PATH"** 체크박스 선택 필수
4. "Install Now" 클릭

### 확인
```bash
python3 --version
# 또는
python --version

# pip 확인
pip3 --version
# 또는
pip --version
```

### 필수 패키지 설치
```bash
# pymysql: DB 연결용
pip3 install pymysql

# python-dotenv: 환경변수 관리용
pip3 install python-dotenv
```

---

## 3. Node.js 설치

### 다운로드 및 설치

**macOS**:
```bash
# Homebrew를 통한 설치 (권장)
brew install node

# 또는 공식 웹사이트에서 다운로드
# https://nodejs.org/
```

**Windows**:
1. [Node.js 공식 웹사이트](https://nodejs.org/) 접속
2. LTS 버전 다운로드 (안정적인 버전)
3. 설치 파일 실행 및 기본 옵션으로 설치

### 확인
```bash
node --version
npm --version
```

---

## 4. Claude Code Extension 설치

### VS Code에서 Extension 설치

1. **VS Code 실행**

2. **Extensions 탭 열기**
   - 단축키: `Cmd+Shift+X` (macOS) / `Ctrl+Shift+X` (Windows)
   - 또는 왼쪽 사이드바의 Extensions 아이콘 클릭

3. **Claude Code 검색 및 설치**
   - 검색창에 "Claude Code" 입력
   - "Claude Code" 또는 "Continue" extension 찾기
   - "Install" 버튼 클릭

   > **참고**: Claude와 연동되는 AI 코딩 어시스턴트로는 다음이 있습니다:
   > - **Continue**: 오픈소스 AI 코딩 어시스턴트
   > - **Cursor**: AI 네이티브 에디터 (VS Code 포크)
   > - **Claude Code CLI**: Anthropic 공식 CLI 도구

4. **API 키 설정**
   - Extension 설치 후 설정 화면에서 Anthropic API 키 입력
   - API 키는 [Anthropic Console](https://console.anthropic.com/)에서 발급

---

## 5. 프로젝트 클론 및 설정

### Git 클론
```bash
# 프로젝트 디렉토리로 이동
cd ~/Documents  # 또는 원하는 위치

# Git 클론
git clone https://github.com/TaebeomHeo/WWAI-HR-01-Internal.git
cd WWAI-HR-01-Internal
```

### VS Code에서 프로젝트 열기
```bash
code .
```

또는 VS Code에서:
1. `File` → `Open Folder`
2. 클론한 프로젝트 폴더 선택

### Database 연결 정보 설정

**Database/.env 파일 생성** (이미 있으면 건너뛰기):

```bash
# Database/.env
DB_HOST=61.37.80.105
DB_PORT=3306
DB_NAME=dbwisewiresdb
DB_USER=wisewires
DB_PASSWORD=<팀 내부 공유 문서 참조>
```

> ⚠️ **주의**: `.env` 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다.

---

## 6. AI로 자연어 조회하기

### hr-db-query-assistant 사용하기

이 프로젝트에는 AI 에이전트가 설정되어 있어 자연어로 데이터베이스를 조회할 수 있습니다.

#### 방법 1: Claude Code CLI 사용

```bash
# Claude Code CLI 설치 (한 번만)
npm install -g @anthropic-ai/claude-code

# AI 에이전트 실행
claude --agent hr-db-query-assistant
```

#### 방법 2: VS Code에서 직접 사용

1. **Command Palette 열기**
   - `Cmd+Shift+P` (macOS) / `Ctrl+Shift+P` (Windows)

2. **Claude Code 또는 Continue 실행**
   - "Claude" 또는 "Continue" 검색
   - Chat 창 열기

3. **Agent 활성화**
   - Agent 메뉴에서 `hr-db-query-assistant` 선택
   - 또는 채팅창에 `@hr-db-query-assistant` 입력

### 자연어 조회 예시

#### 예시 1: 지난주 발령 내역
```
"지난주 발령 내역을 조회해줘"
```

**AI의 처리 과정**:
1. "지난주" → 날짜 범위 계산
2. hrtransferhistory2 View에서 해당 기간 데이터 조회
3. SQL 생성 및 실행
4. 결과를 사람이 읽기 쉬운 형태로 정리

**생성되는 SQL**:
```sql
SET @시작일 = '2025-11-10';
SET @종료일 = '2025-11-16';

SELECT
    employee_number AS 사번,
    name AS 직원명,
    assignment_date AS 발령일,
    assignment_type AS 발령유형,
    division AS 본부,
    team_name AS 팀명,
    project_name AS 프로젝트명
FROM hrtransferhistory2
WHERE assignment_date >= @시작일
  AND assignment_date <= @종료일
ORDER BY assignment_date, name;
```

#### 예시 2: 10월 PL 명단
```
"2025년 10월에 PL이었던 사람들 명단을 조회해줘"
```

**AI의 처리**:
1. 10월 기간 설정 (10/1 ~ 10/31)
2. role = 'PL' 조건 추가
3. 기간 중 하루라도 PL이었으면 포함하는 로직
4. 중복 제거 후 결과 반환

#### 예시 3: 본부별 인원 현황
```
"11월 19일 기준 본부별 팀별 인원 현황을 보여줘"
```

**AI의 처리**:
1. 기준일 설정
2. hrtransferhistory2에서 해당 시점 재직자 필터링
3. 본부, 팀별 GROUP BY
4. 인원수 집계

### AI 조회의 장점

✅ **SQL 문법을 몰라도 됨**: 자연어로 질문하면 됩니다
✅ **날짜 계산 자동**: "지난주", "이번 달" 같은 표현을 자동으로 날짜로 변환
✅ **복잡한 조건 처리**: 기간 겹침, 중복 제거 등 복잡한 로직 자동 처리
✅ **결과 해석**: 단순 데이터가 아닌 해석된 정보 제공
✅ **오류 수정**: SQL 오류 발생 시 자동으로 수정 시도

### 효과적인 질문 방법

#### 좋은 질문 예시
- ✅ "지난주 발령 내역을 조회해줘"
- ✅ "2025년 10월에 PL이었던 사람들을 모두 찾아줘"
- ✅ "현재 개발1본부 소속 인원을 팀별로 보여줘"
- ✅ "이번 달 말에 종료되는 프로젝트 목록"

#### 개선이 필요한 질문 예시
- ❌ "발령" → "지난주 발령 내역" 또는 "최근 발령 현황"
- ❌ "인원" → "본부별 인원 현황" 또는 "팀별 재직자 수"
- ❌ "데이터 줘" → "어떤 데이터를 원하는지 구체적으로 설명"

### 추가 팁

1. **기간 명시**: 조회 기간을 명확히 하면 더 정확한 결과를 얻습니다
2. **단계적 질문**: 복잡한 분석은 단계별로 나눠서 질문
3. **확인 요청**: "결과를 CSV로 저장해줘" 같은 추가 요청 가능
4. **SQL 확인**: AI가 생성한 SQL을 확인하고 SQL-Templates에 저장 가능

---

## 문제 해결

### Python 패키지 설치 오류
```bash
# 권한 오류 시
pip3 install --user pymysql python-dotenv

# 또는 가상환경 사용
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

pip install pymysql python-dotenv
```

### DB 연결 오류
1. `.env` 파일의 비밀번호 확인
2. 네트워크 연결 확인 (VPN 필요한 경우)
3. IP 화이트리스트 등록 여부 확인

### Claude API 키 오류
1. [Anthropic Console](https://console.anthropic.com/)에서 API 키 확인
2. 크레딧 잔액 확인
3. VS Code Extension 설정에서 API 키 재입력

---

## 다음 단계

AI 환경 설정을 완료했다면:
1. **[SQL-Basics](../02-SQL-Basics/)** - SQL 기초 학습
2. **[AI-Usage](../03-AI-Usage/)** - AI와 효과적으로 협업하는 방법
3. **[Real-Cases](../04-Real-Cases/)** - 실제 HR 업무 사례

---

## 참고 자료

- [VS Code 공식 문서](https://code.visualstudio.com/docs)
- [Python 공식 문서](https://docs.python.org/)
- [Node.js 공식 문서](https://nodejs.org/docs/)
- [Claude API 문서](https://docs.anthropic.com/)
- [Continue Extension 문서](https://continue.dev/docs)
