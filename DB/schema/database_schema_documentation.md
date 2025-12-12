# 데이터베이스 스키마 문서

## Tables

### basicinfo

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| nameKOR | varchar(128) | YES |  | None |  |
| nameCHN | varchar(50) | YES |  | None |  |
| nameENG | varchar(128) | YES |  | None |  |
| ppid | varchar(128) | YES |  | None |  |
| birthday | varchar(10) | YES |  | None |  |
| birthkind | varchar(10) | YES |  | None |  |
| firstjoin | char(10) | YES |  | None |  |
| joinreason | varchar(200) | YES |  | None |  |
| retirereason | varchar(200) | YES |  | None |  |
| joinday | char(10) | YES |  | None |  |
| retireday | char(10) | YES |  | None |  |
| companycode | varchar(10) | YES |  | None |  |
| tenurecode | varchar(10) | YES |  | None |  |
| staffkind | varchar(10) | YES |  | None |  |
| dutycode | varchar(10) | YES |  | None |  |
| classcode | varchar(10) | YES |  | None |  |
| positioncode | varchar(10) | YES |  | None |  |
| stationcode | varchar(10) | YES |  | None |  |
| teamcode | varchar(10) | YES |  | None |  |
| telephone1 | varchar(128) | YES |  | None |  |
| mobile | varchar(128) | YES |  | None |  |
| telephone2 | varchar(128) | YES |  | None |  |
| marry | varchar(10) | YES |  | None |  |
| address1 | varchar(128) | YES |  | None |  |
| address2 | varchar(100) | YES |  | None |  |
| postcode | varchar(10) | YES |  | None |  |
| gubncode | varchar(10) | YES |  | None |  |
| workplace | varchar(10) | YES |  | None |  |
| emailaddress | varchar(128) | YES |  | None |  |
| height | varchar(10) | YES |  | None |  |
| weight | varchar(10) | YES |  | None |  |
| eyesightleft | varchar(6) | YES |  | None |  |
| eyesightright | varchar(6) | YES |  | None |  |
| bloodtype | varchar(6) | YES |  | None |  |
| housetype | varchar(10) | YES |  | None |  |
| hobby | varchar(10) | YES |  | None |  |
| comment | varchar(100) | YES |  | None |  |
| firstwriter | char(10) | YES |  | None |  |
| firstwriteday | char(12) | YES |  | None |  |
| lastwriter | char(10) | YES |  | None |  |
| lastwriteday | char(12) | YES |  | None |  |
| ability | varchar(10) | YES |  | None |  |
| religion | varchar(10) | YES |  | None |  |
| partcode | varchar(10) | YES |  | None |  |
| bank1 | varchar(128) | YES |  | None |  |
| bank2 | varchar(128) | YES |  | None |  |
| accountnumber | varchar(128) | YES |  | None |  |
| gender | varchar(10) | YES |  | None |  |
| memberID | varchar(10) | NO | PRI | None |  |
| troubleYN | char(2) | YES |  | None |  |
| troubleNO | varchar(50) | YES |  | None |  |
| troubleName | varchar(100) | YES |  | None |  |
| jobcode | varchar(10) | YES |  | None |  |
| aptitude | varchar(256) | YES |  | None |  |
| invest | varchar(256) | YES |  | None |  |
| groupcode | varchar(10) | YES |  | None |  |
| rejoinYN | varchar(10) | YES |  | None |  |
| workstarttimecode | varchar(10) | YES |  | None |  |
| loginID | varchar(10) | YES |  | None |  |
| CORPGB | int(11) | NO | PRI | 1 |  |
| marryday | varchar(100) | YES |  | None |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | current_timestamp() | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |
| fileNm | varchar(100) | YES |  | None |  |
| filePath | varchar(200) | YES |  | None |  |
| deliverypostcode | varchar(50) | YES |  | None |  |
| deliveryname | char(50) | YES |  | None |  |
| deliveryaddress | char(100) | YES |  | None |  |
| occupationcode | varchar(10) | YES |  | None |  |
| PW | varchar(100) | YES |  | None |  |
| deliveryaddress2 | char(100) | YES |  | None |  |
| AUTH_CD | varchar(50) | YES |  | None |  |
| AUTH_CD_NAME | varchar(100) | YES |  | None |  |
| deliverytelephone | varchar(20) | YES |  | None |  |
| fileSize | int(11) | YES |  | 0 |  |
| sysFileNm | varchar(100) | YES |  | None |  |
| managementyn | varchar(20) | YES |  | None |  |
| PW2 | varchar(100) | YES |  | None |  |

### careerinfo

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| seq | int(11) | NO | PRI | None |  |
| memberID | varchar(10) | NO | PRI | None |  |
| sequencenumber | int(11) | YES |  | None |  |
| schooling | varchar(10) | YES |  | None |  |
| graduation | varchar(10) | YES |  | None |  |
| joinday | varchar(10) | YES |  | None |  |
| retireday | varchar(10) | YES |  | None |  |
| company | varchar(128) | YES |  | None |  |
| classcode | varchar(10) | YES |  | None |  |
| pay | varchar(10) | YES |  | None |  |
| duty | varchar(512) | YES |  | None |  |
| diffdate | int(11) | YES |  | None |  |
| workdate | int(11) | YES |  | None |  |
| workrate | varchar(10) | YES |  | None |  |
| dup | varchar(128) | YES |  | None |  |
| confirm | varchar(10) | YES |  | None |  |
| comment | varchar(512) | YES |  | None |  |
| CORP_GB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | current_timestamp() | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |

### competency_framework

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| id | int(11) | NO | PRI | None | auto_increment |
| competency_code | varchar(500) | NO |  | None |  |
| competency_name_kr | varchar(700) | NO |  | None |  |
| competency_name_en | varchar(700) | NO |  | None |  |
| competency_key | varchar(700) | NO | MUL | None |  |
| category | varchar(100) | NO | MUL | None |  |
| definition | text | YES |  | None |  |
| behavioral_indicators | text | YES |  | None |  |
| sort_order | int(11) | YES |  | 0 |  |
| is_active | tinyint(1) | YES | MUL | 1 |  |
| created_at | timestamp | NO |  | current_timestamp() |  |
| updated_at | timestamp | NO |  | current_timestamp() | on update current_timestamp() |

### conductinfo

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| memberID | varchar(10) | NO | PRI | None |  |
| sequencenumber | int(11) | NO | PRI | None |  |
| maindate | varchar(10) | YES |  | None |  |
| kind | varchar(10) | YES |  | None |  |
| startday | varchar(10) | YES |  | None |  |
| endday | varchar(10) | YES |  | None |  |
| gubncode | varchar(10) | YES |  | None |  |
| reason | varchar(500) | YES |  | None |  |
| condition1 | varchar(10) | YES |  | None |  |
| approvalday | varchar(10) | YES |  | None |  |
| paid | varchar(10) | YES |  | None |  |
| comment | varchar(100) | YES |  | None |  |
| createdate | varchar(10) | YES |  | None |  |
| creategubn | varchar(1024) | YES |  | None |  |
| creatememberid | varchar(10) | YES |  | None |  |
| CORP_GB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | current_timestamp() | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |
| condition | varchar(1024) | YES |  | None |  |

### educationinfo

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| sequencenumber | int(11) | NO | PRI | None |  |
| memberID | varchar(10) | NO | PRI | None |  |
| subject | varchar(10) | NO |  | None |  |
| educationdate | varchar(10) | NO |  | None |  |
| professor | varchar(64) | YES |  | None |  |
| comment | varchar(256) | YES |  | None |  |
| CORP_GB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | current_timestamp() | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |

### gs_h_class

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| HCLASS_CD | varchar(20) | NO | PRI | None |  |
| HCLASS_NM | varchar(50) | YES |  | None |  |
| CD_DESC | varchar(100) | YES |  | None |  |
| ODR | int(11) | YES |  | None |  |
| USE_YN | char(1) | YES |  | None |  |
| REG_ID | varchar(50) | YES |  | None |  |
| DB_INS_TM | timestamp | YES |  | None |  |
| UP_ID | varchar(20) | YES |  | None |  |
| DB_UP_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |
| CORP_GB | int(11) | NO | PRI | None |  |

### gs_m_class

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| MCLASS_CD | varchar(20) | NO |  | None |  |
| HCLASS_CD | varchar(20) | YES | MUL | None |  |
| MCLASS_NM | varchar(1000) | YES |  | None |  |
| CD_DESC | varchar(100) | YES |  | None |  |
| ODR | varchar(10) | YES |  | None |  |
| USE_YN | char(1) | YES |  | None |  |
| REG_ID | varchar(50) | YES |  | None |  |
| DB_INS_TM | timestamp | YES |  | None |  |
| DB_UP_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |
| UP_ID | varchar(20) | YES |  | None |  |
| CORP_GB | int(11) | YES |  | None |  |
| HCLASS_NM | varchar(50) | YES |  | None |  |
| COMMENT | varchar(1000) | YES |  | None |  |

### orderinfo

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| serialnumber | int(11) | NO |  | None |  |
| memberID | varchar(10) | NO | PRI | None |  |
| sequencenumber | int(11) | NO | PRI | None |  |
| kind | varchar(10) | YES |  | None |  |
| orderdate | varchar(10) | YES |  | None |  |
| notifydate | varchar(10) | YES |  | None |  |
| startdate | varchar(10) | YES |  | None |  |
| enddate | varchar(10) | YES |  | None |  |
| companycodeB | varchar(10) | YES |  | None |  |
| positioncodeB | varchar(10) | YES |  | None |  |
| stationcodeB | varchar(10) | YES |  | None |  |
| teamcodeB | varchar(10) | YES |  | None |  |
| partcodeB | varchar(20) | YES |  | None |  |
| dutycodeB | varchar(10) | YES |  | None |  |
| classcodeB | varchar(10) | YES |  | None |  |
| companycodeA | varchar(10) | YES |  | None |  |
| positioncodeA | varchar(10) | YES |  | None |  |
| stationcodeA | varchar(10) | YES |  | None |  |
| teamcodeA | varchar(10) | YES |  | None |  |
| partcodeA | varchar(10) | YES |  | None |  |
| dutycodeA | varchar(10) | YES |  | None |  |
| classcodeA | varchar(10) | YES |  | None |  |
| orderedreason | varchar(512) | YES |  | None |  |
| reason | varchar(512) | YES |  | None |  |
| comment | varchar(128) | YES |  | None |  |
| groupcodeB | varchar(10) | YES |  | None |  |
| groupcodeA | varchar(10) | YES |  | None |  |
| pjcode | int(11) | YES |  | None |  |
| CORP_GB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | current_timestamp() | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |

### performanceevaluation

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| seq | int(11) | NO | PRI | None |  |
| memberid | varchar(16) | NO | PRI | None |  |
| namekor | varchar(64) | YES |  | None |  |
| classcode | varchar(5) | YES |  | None |  |
| classname | varchar(128) | YES |  | None |  |
| dutycode | varchar(10) | YES |  | None |  |
| dutyname | varchar(128) | YES |  | None |  |
| insertdate | varchar(12) | YES |  | None |  |
| updatedate | varchar(12) | YES |  | None |  |
| stationcode | varchar(10) | YES |  | None |  |
| stationname | varchar(128) | YES |  | None |  |
| teamcode | varchar(10) | YES |  | None |  |
| teamname | varchar(128) | YES |  | None |  |
| evaluationID | varchar(16) | YES |  | None |  |
| evaluationName | varchar(128) | YES |  | None |  |
| evaluationContent | varchar(4096) | YES |  | None |  |
| gradecode | varchar(10) | YES |  | None |  |
| gradename | varchar(64) | YES |  | None |  |
| comment | varchar(2048) | YES |  | None |  |
| uploadlog | varchar(512) | YES |  | None |  |
| CORP_GB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | current_timestamp() | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |
| rpkind | varchar(1024) | YES |  | None |  |
| rpreason | varchar(1024) | YES |  | None |  |
| rpcontent | varchar(1024) | YES |  | None |  |
| positioncode | varchar(10) | YES |  | None |  |
| positionname | varchar(128) | YES |  | None |  |

### personalcareer

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| seq | int(11) | NO | PRI | None |  |
| pjcode | int(11) | YES |  | None |  |
| pjname | text | YES |  | None |  |
| memberid | varchar(16) | NO | PRI | None |  |
| namekor | varchar(32) | YES |  | None |  |
| company | varchar(128) | YES |  | None |  |
| customercode | varchar(10) | YES |  | None |  |
| customername | text | YES |  | None |  |
| teamsize | varchar(12) | YES |  | None |  |
| startday | varchar(12) | YES |  | None |  |
| endday | varchar(12) | YES |  | None |  |
| dutycode | varchar(10) | YES |  | None |  |
| dutyname | varchar(64) | YES |  | None |  |
| Mobile | varchar(1) | YES |  | None |  |
| Web | varchar(1) | YES |  | None |  |
| Embedded | varchar(1) | YES |  | None |  |
| SystemInfra | varchar(1) | YES |  | None |  |
| BlackBoxTest | varchar(1) | YES |  | None |  |
| WhiteBoxTest | varchar(1) | YES |  | None |  |
| usinglanguage | text | YES |  | None |  |
| tool | text | YES |  | None |  |
| background | text | YES |  | None |  |
| os | text | YES |  | None |  |
| usingskill | text | YES |  | None |  |
| usingtool | text | YES |  | None |  |
| job | text | YES |  | None |  |
| extrajob | text | YES |  | None |  |
| projectresult | text | YES |  | None |  |
| comment | text | YES |  | None |  |
| groupcomment | text | YES |  | None |  |
| leadercomment | text | YES |  | None |  |
| leaderview | varchar(10) | YES |  | None |  |
| selfcomment | text | YES |  | None |  |
| selfview | varchar(10) | YES |  | None |  |
| partnership | varchar(10) | YES |  | None |  |
| partnercomment | text | YES |  | None |  |
| substitudecode | varchar(10) | YES |  | None |  |
| substitudecomment | text | YES |  | None |  |
| teamcode | varchar(10) | YES |  | None |  |
| teamname | varchar(128) | YES |  | None |  |
| webservice_log | text | YES |  | None |  |
| domain | varchar(10) | YES |  | None |  |
| CORP_GB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | 0000-00-00 00:00:00 | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |
| career | varchar(1) | YES |  | None |  |
| outputPdf | varchar(1) | YES |  | None |  |
| authCdChk | varchar(1) | YES |  | None |  |

### project_candidates

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| id | int(11) | NO | PRI | None | auto_increment |
| name | varchar(100) | NO |  | None |  |
| member_id | varchar(50) | YES |  | None |  |
| career_history | longtext | NO |  | None |  |
| competency_scores | longtext | NO |  | None |  |
| created_at | timestamp | NO |  | current_timestamp() |  |
| updated_at | timestamp | NO |  | current_timestamp() | on update current_timestamp() |

### projectinfo

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| seq | int(11) | NO | PRI | None |  |
| pjcode | varchar(32) | NO | PRI | 1 |  |
| pjname | varchar(512) | NO |  | None |  |
| pjstatus | varchar(10) | NO |  | None |  |
| startday | varchar(12) | YES |  | None |  |
| endday | varchar(12) | YES |  | None |  |
| company | varchar(256) | YES |  | None |  |
| address | varchar(512) | YES |  | None |  |
| intime | varchar(12) | YES |  | None |  |
| outtime | varchar(12) | YES |  | None |  |
| stationcode | varchar(10) | YES |  | None |  |
| stationname | varchar(128) | YES |  | None |  |
| teamcode | varchar(10) | YES |  | None |  |
| teamname | varchar(128) | YES |  | None |  |
| teamcode1 | varchar(10) | YES |  | None |  |
| teamname1 | varchar(128) | YES |  | None |  |
| teamcode2 | varchar(10) | YES |  | None |  |
| teamname2 | varchar(128) | YES |  | None |  |
| teamcode3 | varchar(10) | YES |  | None |  |
| teamname3 | varchar(128) | YES |  | None |  |
| teamcode4 | varchar(10) | YES |  | None |  |
| teamname4 | varchar(128) | YES |  | None |  |
| teamcode5 | varchar(10) | YES |  | None |  |
| teamname5 | varchar(128) | YES |  | None |  |
| pjleader | varchar(64) | YES |  | None |  |
| pjleadername | varchar(128) | YES |  | None |  |
| majorjob | text | YES |  | None |  |
| customercode | varchar(10) | YES |  | None |  |
| customername | varchar(512) | YES |  | None |  |
| customertel | varchar(128) | YES |  | None |  |
| activeYN | varchar(10) | YES |  | None |  |
| Mobile | varchar(10) | YES |  | None |  |
| Web | varchar(10) | YES |  | None |  |
| Embedded | varchar(10) | YES |  | None |  |
| SystemInfra | varchar(10) | YES |  | None |  |
| BlackBoxTest | varchar(10) | YES |  | None |  |
| WhiteBoxTest | varchar(10) | YES |  | None |  |
| comment | varchar(1024) | YES |  | None |  |
| commenthistory | varchar(2048) | YES |  | None |  |
| pjleader1 | varchar(64) | YES |  | None |  |
| pjleadername1 | varchar(128) | YES |  | None |  |
| pjleader2 | varchar(64) | YES |  | None |  |
| pjleadername2 | varchar(128) | YES |  | None |  |
| pjleader3 | varchar(64) | YES |  | None |  |
| pjleadername3 | varchar(128) | YES |  | None |  |
| pjleader4 | varchar(64) | YES |  | None |  |
| pjleadername4 | varchar(128) | YES |  | None |  |
| pjleader5 | varchar(64) | YES |  | None |  |
| pjleadername5 | varchar(128) | YES |  | None |  |
| usinglanguage | varchar(512) | YES |  | None |  |
| tool | varchar(512) | YES |  | None |  |
| background | varchar(512) | YES |  | None |  |
| os | varchar(512) | YES |  | None |  |
| usingskill | varchar(1024) | YES |  | None |  |
| usingtool | varchar(1024) | YES |  | None |  |
| teamsize | varchar(12) | YES |  | None |  |
| domain | varchar(10) | YES |  | None |  |
| CORPGB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(60) | YES |  | None |  |
| UPD_TM | timestamp | YES |  | None |  |
| REG_TM | timestamp | YES |  | None |  |
| positioncode | varchar(10) | YES |  | None |  |
| positionname | varchar(128) | YES |  | None |  |
| ProfessionalEngineer | varchar(20) | YES |  | None |  |
| Expert | varchar(20) | YES |  | None |  |
| Advanced | varchar(20) | YES |  | None |  |
| Intermediate | varchar(20) | YES |  | None |  |
| Beginner | varchar(20) | YES |  | None |  |

### qualification_req

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| seq | int(11) | NO | PRI | None | auto_increment |
| OCCUPATION_CODE | varchar(10) | YES |  | None |  |
| OCCUPATION_NAME | varchar(50) | YES |  | None |  |
| QUALIFICATION | varchar(500) | YES |  | None |  |
| FUNCTIONNAME | varchar(200) | YES |  | None |  |
| ODR | int(11) | YES |  | None |  |
| USE_YN | char(2) | YES |  | None |  |
| CORP_GB | int(11) | YES |  | 0 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | 0000-00-00 00:00:00 | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |
| EVALUATEYN | char(2) | YES |  | None |  |
| CERTIFICATEYN | char(2) | YES |  | None |  |
| CHECKBOXYN | char(2) | YES |  | None |  |

### qualificationinfo

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| memberID | varchar(10) | NO | PRI | None |  |
| sequencenumber | int(11) | NO | PRI | None |  |
| code | varchar(10) | YES |  | None |  |
| names | varchar(50) | YES |  | None |  |
| gainday | varchar(10) | YES |  | None |  |
| serialnumber | varchar(30) | YES |  | None |  |
| grade | varchar(30) | YES |  | None |  |
| kind | varchar(10) | YES |  | None |  |
| period | varchar(10) | YES |  | None |  |
| government | varchar(10) | YES |  | None |  |
| comment | varchar(100) | YES |  | None |  |
| CORP_GB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | current_timestamp() | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |

### scholarshipinfo

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| memberID | varchar(10) | NO | PRI | None |  |
| sequencenumber | decimal(18,0) | NO | PRI | None |  |
| schooling | char(10) | YES |  | None |  |
| schoolname | varchar(40) | YES |  | None |  |
| entrance | char(10) | YES |  | None |  |
| graduation | char(10) | YES |  | None |  |
| majorname | varchar(50) | YES |  | None |  |
| address | varchar(50) | YES |  | None |  |
| comment | varchar(100) | YES |  | None |  |
| finalYN | char(1) | YES |  | None |  |
| CORP_GB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | current_timestamp() | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |

### specialtyinfo

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| sequencenumber | int(11) | NO | PRI | None |  |
| memberID | varchar(10) | NO | PRI | None |  |
| specialty | varchar(10) | NO |  | None |  |
| spercent | int(11) | NO |  | None |  |
| comment | varchar(128) | YES |  | None |  |
| CORP_GB | int(11) | NO | PRI | 1 |  |
| REG_ID | varchar(50) | YES |  | None |  |
| UPD_ID | varchar(50) | YES |  | None |  |
| UPD_TM | timestamp | NO |  | current_timestamp() | on update current_timestamp() |
| REG_TM | timestamp | NO |  | 0000-00-00 00:00:00 |  |

## Views

### basicinfoview

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| name_kor | varchar(128) | YES |  |  |  |
| name_eng | varchar(128) | YES |  |  |  |
| birth_date | varchar(10) | YES |  |  |  |
| join_date | char(10) | YES |  |  |  |
| position_code | varchar(10) | YES |  |  |  |
| team_code | varchar(10) | YES |  |  |  |
| mobile_number | varchar(128) | YES |  |  |  |
| telephone_primary | varchar(128) | YES |  |  |  |
| address | varchar(128) | YES |  |  |  |
| email_address | varchar(128) | YES |  |  |  |
| member_id | varchar(10) | NO |  |  |  |
| role | varchar(100) | YES |  |  |  |
| corp | varchar(7) | NO |  |  |  |
| CORPGB | int(11) | NO |  | 1 |  |
| current_project_code | varchar(32) | YES |  | 1 |  |
| current_project_name | varchar(512) | YES |  |  |  |
| current_project_start_date | varchar(12) | YES |  |  |  |
| current_project_end_date | varchar(12) | YES |  |  |  |
| current_project_status | varchar(10) | YES |  |  |  |

### careerview

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| project_name | text | YES |  |  |  |
| project_code | int(11) | YES |  |  |  |
| member_id | varchar(16) | NO |  |  |  |
| name_kor | varchar(32) | YES |  |  |  |
| company | varchar(128) | YES |  |  |  |
| customer | text | YES |  |  |  |
| team_size | varchar(12) | YES |  |  |  |
| start_date | varchar(12) | YES |  |  |  |
| end_date | varchar(12) | YES |  |  |  |
| role | varchar(64) | YES |  |  |  |
| project_type | varchar(44) | YES |  |  |  |
| test_type | varchar(30) | YES |  |  |  |
| skill_set | mediumtext | YES |  |  |  |
| job | text | YES |  |  |  |
| extra_job | mediumtext | YES |  |  |  |
| project_result | mediumtext | YES |  |  |  |
| comment | mediumtext | YES |  |  |  |
| project_domain | varchar(10) | YES |  |  |  |
| project_major_job | text | YES |  |  |  |
| team_name | varchar(128) | YES |  |  |  |

### hrtransferhistory

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| employee_number | varchar(10) | NO |  |  |  |
| name | varchar(128) | YES |  |  |  |
| assignment_date | varchar(10) | YES |  |  |  |
| assignment_type | text | YES |  |  |  |
| end_date | varchar(10) | NO |  |  |  |
| project_duration | int(7) | YES |  |  |  |
| role | text | YES |  |  |  |
| division | text | YES |  |  |  |
| team_code | varchar(10) | YES |  |  |  |
| team_name | text | YES |  |  |  |
| client_company | varchar(256) | YES |  |  |  |
| project_name | varchar(512) | YES |  |  |  |
| project_code | varchar(32) | YES |  | 1 |  |
| project_start_date | varchar(12) | YES |  |  |  |
| project_end_date | varchar(12) | YES |  |  |  |
| available_after_date | varchar(12) | NO |  |  |  |

### hrtransferhistory2

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| employee_number | varchar(10) | YES |  |  |  |
| name | varchar(128) | YES |  |  |  |
| assignment_date | varchar(10) | YES |  |  |  |
| assignment_type | text | YES |  |  |  |
| end_date | varchar(10) | NO |  |  |  |
| project_duration | int(7) | YES |  |  |  |
| role | text | YES |  |  |  |
| division | text | YES |  |  |  |
| team_code | varchar(10) | YES |  |  |  |
| team_name | text | YES |  |  |  |
| client_company | varchar(256) | YES |  |  |  |
| project_name | varchar(512) | YES |  |  |  |
| project_code | varchar(32) | YES |  | 1 |  |
| project_start_date | varchar(12) | YES |  |  |  |
| project_end_date | varchar(12) | YES |  |  |  |
| available_after_date | varchar(12) | NO |  |  |  |

### projectinfoview

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| project_code | varchar(32) | NO |  | 1 |  |
| project_name | varchar(512) | NO |  |  |  |
| start_date | varchar(12) | YES |  |  |  |
| end_date | varchar(12) | YES |  |  |  |
| customer | varchar(512) | YES |  |  |  |
| project_address | varchar(512) | YES |  |  |  |
| team_code | varchar(10) | YES |  |  |  |
| team_name | varchar(128) | YES |  |  |  |
| project_leader | varchar(64) | YES |  |  |  |
| project_leader_name | varchar(128) | YES |  |  |  |
| initial_major_job | text | YES |  |  |  |
| active_status | varchar(10) | YES |  |  |  |
| project_type | varchar(44) | YES |  |  |  |
| test_type | varchar(30) | YES |  |  |  |
| initial_skill_set | text | YES |  |  |  |
| team_size | varchar(12) | YES |  |  |  |
| project_domain | varchar(10) | YES |  |  |  |
| major_job | mediumtext | YES |  |  |  |
| skill_set | mediumtext | YES |  |  |  |

### scholarshipview

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| memberid | varchar(10) | NO |  |  |  |
| nameKOR | varchar(128) | YES |  |  |  |
| nameENG | varchar(128) | YES |  |  |  |
| schooling | text | YES |  |  |  |
| schoolname | varchar(40) | YES |  |  |  |
| majorname | varchar(50) | YES |  |  |  |
| entrance | varchar(10) | YES |  |  |  |
| graduation | varchar(10) | YES |  |  |  |

### v_candidate_summary

| Column Name | Type | Null | Key | Default | Extra |
|-------------|------|------|-----|---------|-------|
| id | int(11) | NO |  | 0 |  |
| name | varchar(100) | NO |  |  |  |
| member_id | varchar(50) | YES |  |  |  |
| career_summary | varchar(100) | NO |  |  |  |
| evaluation_date | longtext | YES |  |  |  |
| created_at | timestamp | NO |  | current_timestamp() |  |

