# Saramin Talent Search Automated Implementation Task List

- [x] **Step 1: Authentication (Login)**
  - [x] Logic creation (`src/saramin_bot.py`).
  - [x] Corporate Member Login (ID/PW injection).
  - [x] Verification of successful login (URL transition).
  - [x] `instruction_saramin.md`: Default selectors confirmed.

- [/] **Step 2: Talent Search Logic (Search)**
  - [x] **Search UI Analysis**:
    - [x] Identify OR Input: `.search_default input.search_input`
    - [x] Identify 'Exact Match' Toggle: `label[for="keywordSearch"]` (Input `#keywordSearch` is hidden).
  - [/] **Basic Search Verification**:
    - [x] English Keyword ("SQA", "QA"): Success.
    - [ ] **Hangul Keyword ("개발"): FAILED (Simulated Typing/JS Input issues).** -> **Needs Debugging**
  - [ ] **Advanced Search Conditions**:
    - [ ] AND Condition: Verify `.search_word_include` input behavior.
    - [ ] NOT Condition: Verify `.search_word_except` behavior.
  - [ ] **Filters**:
    - [ ] Career (5yr+), Region, etc.

- [ ] **Step 3: Data Extraction (Extraction)**
  - [ ] Extract Top 10 Candidates.
  - [ ] Field Mapping verification (Name, Title, Experience, Link).
  - [ ] Pagination handling (if needed).

- [ ] **Final Polish**
  - [ ] Full E2E Workflow Loop.
  - [ ] `instruction_saramin.md` Finalization.
