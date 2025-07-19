import streamlit as st
import pandas as pd
from io import StringIO

st.title("📋 엑셀 데이터 붙여넣기 (투입물 입력)")

# 설명
st.markdown("""
1. 엑셀에서 **물질명 ~ 국가까지** 복사 (`Ctrl+C`)
2. 아래 텍스트박스에 `Ctrl+V`로 붙여넣기
3. 자동으로 테이블로 변환됨
""")

# 붙여넣기 입력창
user_input = st.text_area("엑셀에서 복사한 내용 붙여넣기", height=200)

# 변환 시도
if user_input:
    try:
        # 탭 또는 쉼표로 구분된 데이터 판별
        sep = '\t' if '\t' in user_input else ','

        df = pd.read_csv(StringIO(user_input), sep=sep)

        st.success("✅ 테이블 변환 성공!")
        st.dataframe(df)

        # 저장 버튼
        if st.button("📁 CSV로 저장"):
            df.to_csv("붙여넣은_투입물.csv", index=False)
            st.success("CSV 파일로 저장 완료!")

    except Exception as e:
        st.error(f"❌ 변환 실패: {e}")
else:
    st.info("⏳ 엑셀에서 데이터를 복사한 뒤 여기에 붙여넣어 주세요.")
