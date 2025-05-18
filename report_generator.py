import streamlit as st
import openai
import os

# openai_api_key를 api_key.txt에서 읽어오기
openai_api_key = st.secrets["OPENAI_API_KEY"]
if os.path.exists(api_key_path):
    with open(api_key_path, 'r', encoding='utf-8') as f:
        openai_api_key = f.read().strip()

st.title("  자동 업무보고서 생성기")

# 타이틀/목차 입력 예시 이미지 추가
st.image('example.png', caption=None)
st.markdown("<span style='color:red; font-weight:bold;'>위 예시를 참고해서 입력</span>", unsafe_allow_html=True)
# 타이틀(목차) 입력
st.markdown("#### 타이틀/목차를 입력하세요")
title = st.text_area("타이틀/목차 입력", height=200)

# 분량 선택
length_option = st.selectbox(
    "원하는 분량을 선택하세요",
    ("A4 반장 (약 600자)", "A4 1장 (약 1200자)", "A4 2장 (약 1400자)")
)

if length_option == "A4 반장 (약 600자)":
    char_count = 600
elif length_option == "A4 1장 (약 1200자)":
    char_count = 1200
else:
    char_count = 1400

if st.button("보고서 생성하기"):
    if not title.strip():
        st.warning("타이틀/목차를 입력해주세요.")
    elif not openai_api_key:
        st.error("OpenAI API 키가 api_key.txt에 설정되어 있지 않습니다.")
    else:
        with st.spinner("보고서를 생성 중입니다..."):
            prompt = f"""
            아래의 목차에 따라 지방자치단체 기획 업무보고서를 작성해줘.

            - 목차: {title}
            - 반드시 {char_count}자에 최대한 가깝게 작성해줘. 글자수가 부족하면 추가로 더 길게, 충분히 자세히 작성해줘. {char_count}자에 최대한 근접하게 작성해줘.
            - 2023년, 2024년, 2025년년 기준 최신 정책, 통계, 트렌드, 법령 등 최신 정보를 반영해서 작성해줘.
            - 최근의 사회적 이슈와 정책 방향을 중심으로 작성해줘.
            - 지방자치단체 기획 전문가의 시각에서, 실무적으로 신뢰성 있게 작성해줘.
            - 각 항목별로 개조식(글머리표)으로 작성하되, 각 bullet point는 1~2줄로 작성해줘.
            - 각 항목별로 2~5개 정도로로 bullet point로 작성해줘.
            - 불필요한 서론, 결론 없이 바로 항목별로 시작해줘.
            - 만약 '관련법' 항목이 있다면, 해당 주제와 연관된 대한민국 법령을 간략하게 요약해서 포함해줘.
            - 모든 bullet point의 끝맺음 표현은 '있음', '였음' 이런 형태로 작성해줘. 
            - 반드시 {char_count}자에 최대한 가깝게 작성해줘.
            """
            client = openai.OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=min(char_count * 3, 4096),
                temperature=0.7,
            )
            report = response.choices[0].message.content
            st.text_area("생성된 보고서", report, height=500)
            st.download_button("보고서 다운로드", report, file_name="report.txt")

st.markdown("---")
