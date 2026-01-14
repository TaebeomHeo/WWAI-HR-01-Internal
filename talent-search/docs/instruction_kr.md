# 잡코리아 인재 검색 - AI 지침 매뉴얼

이 문서는 AI 에이전트가 잡코리아에서 인재 검색을 수행하기 위한 표준 운영 절차(SOP)입니다.

## 1. 입력 변수 (Input Variables)

이 지침을 실행할 때, 사용자는 다음 정보를 제공해야 합니다:

- **대상 키워드 (Target Keyword)**: (예: "SQA", "재무", "Java")
- **검색 날짜 (Search Date)**: (YYYY-MM-DD 형식의 오늘 날짜)

## 2. 사전 요구사항 (Pre-requisites)

- **인증 자격 증명 (Credentials)**:
  - ID: `wisewires9`
  - PW: `insa5051`
- **도구 (Tools)**: 브라우저 도구 (Headful/Headless), 파일 시스템.

## 3. 실행 단계 (Execution Steps)

### 1단계: 로그인 (기업회원)

1.  브라우저를 열고 `https://www.jobkorea.co.kr/Login/Login_Tot.asp`로 이동합니다.
2.  **"기업회원"** 탭을 클릭합니다.
3.  ID와 비밀번호를 입력합니다.
4.  로그인 버튼을 클릭합니다.
5.  **확인**: 메인 대시보드로 리디렉션되거나 "로그아웃" 버튼이 있는지 확인합니다.

### 2단계: 검색

1.  **인재 검색** 페이지로 이동: `https://www.jobkorea.co.kr/Corp/Person/Find`
2.  **키워드 입력**:
    - **목표**: "SQA"(일치)와 "금융/은행"(통합) 키워드를 모두 만족하는 후보자 찾기.
    - **방법 A (권장 - "결과 내 재검색")**:
      1.  먼저 **"SQA"**를 **"일치검색"**으로 검색합니다.
      2.  결과 페이지에서 **"결과 내 재검색"** 체크박스(보통 검색창 근처)를 확인합니다.
      3.  **"금융"** (또는 2차 목표 키워드)을 입력하고 검색합니다.
      4.  **중요**: 영어/표준 키워드는 타이핑하되, 한글 키워드의 경우 자동화 입력이 실패하면 직접 타이핑 대신 클립보드/값 주입(Value Injection) 방식을 사용하십시오.
    - **방법 B (대안)**: "상세검색" 사용 > "일치검색" 필드에 "SQA" 입력, "키워드" 필드에 "금융" 입력.
3.  **검색 버튼**을 클릭합니다.
4.  결과가 로드될 때까지 기다립니다.

### 3단계: 스크랩 (Scrap - 신규 추가)

> **사용자 요청**: 상위 10명의 인재에 대해 "스크랩" 버튼을 클릭하여 저장합니다.

1.  **동작**: 검색 결과 목록에서 상위 10명의 후보자를 순회하며 스크랩 버튼을 클릭합니다.
2.  **구현 로직 (JS)**:

    - **주의**: 스크랩 버튼 클릭 시 **팝업**이 발생하므로, 단순 클릭만으로는 저장되지 않습니다. 반드시 아래의 **폴더 선택** 로직을 따라야 합니다.

    **구현 로직 (JS - Async/Await 사용 권장)**:

    ```javascript
    const scrapCandidate = async (btn) => {
      btn.click();

      // 1. 팝업 대기 (약 1초 안전 대기)
      await new Promise((r) => setTimeout(r, 1000));
      const popup = document.querySelector(
        '.devScrapPopup, #devScrapPopup, .popup-scrap'
      );

      if (!popup) {
        console.warn('Popup did not appear');
        return;
      }

      // 2. 탭 선택: "기본인재풀 폴더" (텍스트 매칭으로 찾기)
      const tabs = Array.from(popup.querySelectorAll('a, button, li'));
      const basicTab = tabs.find((t) => t.innerText.includes('기본인재풀'));
      if (basicTab) {
        basicTab.click();
        await new Promise((r) => setTimeout(r, 500)); // 탭 전환 대기
      }

      // 3. 폴더 선택: 'AI' 폴더
      // 드롭다운이나 리스트에서 'AI' 텍스트를 가진 항목을 찾아 클릭
      // (단순 클릭으로 안 될 경우, select value 변경 로직 필요할 수 있음)
      const options = Array.from(popup.querySelectorAll('li, option, a'));
      const aiOption = options.find((o) => o.innerText.trim() === 'AI');

      if (aiOption) {
        aiOption.click();
        // 만약 option 태그라면 부모 select의 값도 변경 시도
        if (aiOption.tagName === 'OPTION' && aiOption.parentElement) {
          aiOption.parentElement.value = aiOption.value;
          aiOption.parentElement.dispatchEvent(new Event('change'));
        }
      } else {
        console.warn("'AI' folder not found");
      }

      await new Promise((r) => setTimeout(r, 500));

      // 4. 확인(스크랩) 버튼 클릭
      const confirmBtn = Array.from(popup.querySelectorAll('button')).find(
        (b) => b.innerText.trim() === '스크랩' || b.innerText.trim() === '확인'
      );
      if (confirmBtn) confirmBtn.click();

      // 5. 완료 대기
      await new Promise((r) => setTimeout(r, 1000));
    };

    (async () => {
      const buttons = Array.from(
        document.querySelectorAll('button.devButtonScrap, button.btnScrap')
      ).slice(0, 10);
      let count = 0;

      for (const [index, btn] of buttons.entries()) {
        // 이미 스크랩된 경우(.on 등) 건너뜀
        if (
          !btn.classList.contains('on') &&
          !btn.classList.contains('active')
        ) {
          console.log(`[${index + 1}] Processing scrap...`);
          await scrapCandidate(btn);
          count++;
        }
      }
      console.log(`${count} candidates processed.`);
    })();
    ```

### 4단계: 추출 및 출력 (Extraction & Output)

1.  후보자 목록을 식별합니다.
2.  **상위 10명 후보자**에 대해 다음 필드를 추출합니다:
    - **이름 (Name)**: (예: 홍길동)
    - **정보/직함 (Info/Title)**: (예: X회사 QA 팀장)
    - **경력 (Experience)**: (예: 10년 2개월)
    - **링크 (Link)**: (이력서 전체 URL)
3.  데이터를 CSV 파일로 포맷팅합니다.
    - **파일명**: `candidate_list_{Date}_{Keyword}.csv`
    - **경로**: `talent-search/candidate/`
    - **헤더**: `Name, Title, Experience, Link`

## 4. 완료 (Completion)

- 생성된 CSV 파일의 경로를 사용자에게 알립니다.
