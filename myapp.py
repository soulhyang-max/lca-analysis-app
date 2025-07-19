import streamlit as st
import pandas as pd

st.set_page_config(layout="wide") # 넓은 레이아웃으로 설정

st.title("원부자재 입력 및 LCA 분석 도구")

st.header("원부자재 입력")

# 초기 데이터프레임 생성 (사용자 입력을 받을 테이블)
# '분류' 컬럼에 기본값을 설정하거나 비워둘 수 있습니다.
data = {
    "물질명": ["" for _ in range(10)],  # 10개의 빈 행을 초기화
    "분류": ["" for _ in range(10)], # '분류' 컬럼
    "투입량(kg/km)": ["" for _ in range(10)],
    "연결 DB명": ["" for _ in range(10)],
    "국가": ["" for _ in range(10)],
}
df = pd.DataFrame(data)

# st.data_editor를 사용하여 테이블 형태의 입력 받기
# num_rows="dynamic"을 사용하면 사용자가 행을 추가/삭제할 수 있습니다.
edited_df = st.data_editor(
    df,
    num_rows="dynamic", # 행 추가/삭제 기능 활성화
    column_config={
        "물질명": st.column_config.TextColumn(
            "물질명",
            help="물질명을 입력하세요.",
            required=True,
        ),
        "분류": st.column_config.SelectboxColumn( # SelectboxColumn으로 변경
            "분류",
            help="물질의 분류를 선택하세요.",
            options=["", "원료물질", "보조물질"], # 선택 가능한 옵션
            required=False, # 필수가 아닐 경우
        ),
        "투입량(kg/km)": st.column_config.NumberColumn(
            "투입량(kg/km)",
            help="투입량을 kg/km 단위로 입력하세요.",
            min_value=0.0,
            format="%f",
            required=True,
        ),
        "연결 DB명": st.column_config.TextColumn(
            "연결 DB명",
            help="연결될 DB 이름입니다. (자동 선택 예정)",
            disabled=True,
        ),
         "국가": st.column_config.TextColumn(
            "국가",
            help="물질의 국가를 입력하세요.",
        ),
    },
    hide_index=True,
    key="material_input_editor"
)

st.write("---")
st.subheader("입력된 원부자재 목록 (확인용)")
st.dataframe(edited_df)

# 사용자가 입력한 데이터를 추출하고 처리하는 부분
# 여기서는 단순히 출력만 하지만, 실제 LCA 분석 로직은 이 아래에 추가됩니다.
if not edited_df.empty:
    # '물질명'과 '투입량(kg/km)'이 입력된 유효한 행만 필터링
    # 빈 문자열, NaN, None 등을 False로 간주하여 필터링합니다.
    valid_inputs = edited_df[
        edited_df["물질명"].astype(bool) &
        edited_df["투입량(kg/km)"].astype(bool)
    ]

    if not valid_inputs.empty:
        st.subheader("LCA 분석 준비 중...")
        st.write("다음 물질들을 분석할 예정입니다:")
        st.dataframe(valid_inputs[['물질명', '분류', '투입량(kg/km)']]) # 분류 컬럼 추가

        # TODO: 여기에 '물질명'을 기반으로 '연결 DB명'을 자동으로 선택하는 로직을 추가
        # 예시:
        # for index, row in valid_inputs.iterrows():
        #     물질명 = row['물질명']
        #     # 데이터베이스나 딕셔너리에서 물질명에 해당하는 연결DB명 찾기
        #     연결_DB명 = your_db_lookup_function(물질명)
        #     # edited_df의 해당 행에 연결_DB명 업데이트 (이 부분은 edited_df가 다시 렌더링되어야 반영됨)
        #     # 실제 앱에서는 이 부분을 버튼 클릭 이벤트 등으로 처리하여 업데이트하거나,
        #     # 별도의 처리된 결과를 보여주는 것이 좋습니다.

        st.info("LCA 분석 로직은 아직 구현되지 않았습니다. '연결 DB명' 자동 선택 및 LCA 분석 기능을 추가할 예정입니다.")
    else:
        st.warning("물질명과 투입량을 입력해주세요.")
else:
    st.info("원부자재를 입력해주세요.")

# 필요에 따라 추가적인 버튼이나 기능들을 여기에 배치할 수 있습니다.
if st.button("LCA 분석 시작 (미구현)"):
    st.write("LCA 분석 기능은 추후 추가될 예정입니다.")