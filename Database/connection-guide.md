# HR 데이터베이스 연결 가이드

## 연결 정보

DBeaver에서 새 연결 생성 시 다음 정보를 입력하세요:

| 항목 | 값 |
|------|-----|
| Server Host | 61.37.80.105 |
| Port | 3306 |
| Database | dbwisewiresdb |
| Username | wisewires |
| Password | (관리자에게 문의) |

## 연결 방법

1. DBeaver 실행
2. 상단 메뉴에서 "New Database Connection" 클릭 (또는 `Ctrl+N`)
3. **MySQL** 선택 후 "Next"
4. 위 연결 정보 입력
5. "Test Connection" 클릭하여 연결 확인
6. "Finish" 클릭

## 연결 오류 시

- **VPN 필요 여부**: 사내 네트워크 또는 VPN 연결 필요할 수 있음
- **방화벽**: 3306 포트 허용 필요
- **계정 문제**: 관리자에게 계정 활성화 확인 요청

## CLI 연결 (고급)

터미널에서 직접 연결하려면:

```bash
mysql -h 61.37.80.105 -P 3306 -u wisewires -p dbwisewiresdb
```

비밀번호 입력 프롬프트가 나타나면 비밀번호를 입력하세요.
