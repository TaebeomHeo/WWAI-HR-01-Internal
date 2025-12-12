import pandas as pd
import re

# Raw data extracted from browser tool
data = [
  {"name":"구휘모", "metadata":"남 만 26세 "},
  {"name":"연태준", "metadata":"남 만 25세 "},
  {"name":"한태균", "metadata":"남 만 26세 "},
  {"name":"정재윤", "metadata":"남 만 23세 "},
  {"name":"주현우", "metadata":"남 만 25세 "},
  {"name":"김태현", "metadata":"남 만 27세 "},
  {"name":"전혜진", "metadata":"여 만 34세 "},
  {"name":"오영찬", "metadata":"남 만 22세 "},
  {"name":"김이영", "metadata":"남 만 26세 "},
  {"name":"강태훈", "metadata":"남 만 28세 "},
  {"name":"임지현", "metadata":"여 만 23세 "},
  {"name":"노희일", "metadata":"남 만 26세 "},
  {"name":"박예현", "metadata":"남 만 25세 "},
  {"name":"이태윤", "metadata":"남 만 28세 "},
  {"name":"이민재", "metadata":"남 만 28세 "},
  {"name":"NaJared", "metadata":"남 만 22세 "},
  {"name":"양지은", "metadata":"여 만 28세 "},
  {"name":"강윤선", "metadata":"여 만 25세 "},
  {"name":"유동환", "metadata":"남 만 26세 "},
  {"name":"정병훈", "metadata":"남 만 25세 "},
  {"name":"정도우", "metadata":"남 만 28세 "}
]

cleaned_data = []

for item in data:
    name = item['name']
    meta = item['metadata']
    
    # Simple regex to extract common fields
    # Example meta: "남 만 26세 대졸(4년) 경력 2년" (It varies)
    
    # Gender
    gender = "Unknown"
    if "남" in meta: gender = "남"
    elif "여" in meta: gender = "여"
    
    # Age (e.g. "만 26세")
    age = ""
    age_match = re.search(r'만\s*(\d+)세', meta)
    if age_match:
        age = age_match.group(1)
        
    # Education (Heuristic: typical Korean edu terms)
    education = ""
    edu_terms = ["대졸", "초대졸", "고졸", "대학원", "박사", "석사"]
    for term in edu_terms:
        if term in meta:
             # Try to capture context like "대졸(4년)"
             # Find the term and grab nicely
             edu_match = re.search(rf'({term}[^\s]*)', meta)
             if edu_match:
                 education = edu_match.group(1)
             else:
                 education = term
             break
    
    # Career
    career = "신입"
    if "경력" in meta:
        career_match = re.search(r'경력\s*([^\s]+)', meta)
        if career_match:
            career = "경력 " + career_match.group(1)
    
    cleaned_data.append({
        "이름": name,
        "성별": gender,
        "나이": age,
        "학력": education,
        "경력": career,
        "원본_메타데이터": meta
    })

df = pd.DataFrame(cleaned_data)
output_file = "jobkorea_applicants_detailed.xlsx"
df.to_excel(output_file, index=False)
print(f"Saved {len(cleaned_data)} applicants to {output_file}")
