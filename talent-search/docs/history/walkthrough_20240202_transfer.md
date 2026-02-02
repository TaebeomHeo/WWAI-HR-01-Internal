# Saramin Talent Search - Verification Log

## 1. Authentication

- **Status**: ✅ Success
- **Method**: Verified login with `wisewires` account.
- **Selectors**:
  - Corporate Tab: `.btn_tab.t_com`
  - ID/PW: `#id`, `#password`

## 2. Search Interaction (Basic)

- **Status**: ⚠️ Partial Success
- **Verified Selectors**:
  - **OR Input**: `.search_default input.search_input`
  - **Exact Match Toggle**: `label[for="keywordSearch"]`
    - _Note_: Clicking the checkbox directly or the "Search Options" title fails. Must target the `label`.

### Test Cases

| Case | Keyword | Exact Match | Result  | Notes                                                 |
| ---- | ------- | ----------- | ------- | ----------------------------------------------------- |
| 1    | "SQA"   | ON          | ✅ Pass | Results loaded correctly.                             |
| 2    | "QA"    | ON          | ✅ Pass | Results loaded correctly.                             |
| 3    | "개발"  | ON          | ❌ Fail | Browser automation timeout/error during Hangul input. |

## 3. Current Blocker: Hangul Input

- **Issue**: Standard `browser_press_key` fails for Hangul characters. JS injection (`input.value = '...'`) triggered browser disconnects/timeouts in the subagent environment.
- **Next Steps**:
  1.  Debug Hangul input (Try Clipboard Paste method or robust JS event sequences).
  2.  Verify "AND" condition input (may face same Hangul issue).

## 4. Remaining Scope

- **AND/NOT Logic**: Verify selectors and input.
- **Filters**: Verify Apply action.
- **Extraction**: Verify DOM parsing for candidate cards.
