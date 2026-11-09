import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="글로벌 MBTI 국가별 분포 시각화", page_icon="🌍", layout="wide"
)

# MBTI 16가지 컬럼 정의
MBTI_TYPES = [
    "INFJ",
    "ISFJ",
    "INTP",
    "ISFP",
    "ENTP",
    "INFP",
    "ENTJ",
    "ISTP",
    "INTJ",
    "ESFP",
    "ESTJ",
    "ENFP",
    "ESTP",
    "ISTJ",
    "ENFJ",
    "ESFJ",
]


@st.cache_data
def load_data():
  file_path = "countriesMBTI_16types.csv"
  if os.path.exists(file_path):
    return pd.read_csv(file_path)
  return None


df = load_data()

st.title("🌍 국가별 MBTI 분포 시각화 대시보드")
st.markdown(
    "선택한 국가의 MBTI 유형별 비율을 확인해보세요. **1등 유형은 핑크색**, 2등부터는 **파란색"
    " 그라데이션**으로 표시됩니다."
)
st.markdown("---")

if df is None:
  st.error(
      "⚠️ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 저장소 루트 경로에"
      " CSV 파일을 함께 업로드해주세요."
  )
  uploaded = st.file_uploader("CSV 파일 업로드", type=["csv"])
  if uploaded is not None:
    df = pd.read_csv(uploaded)
  else:
    st.stop()

# 1. 국가 선택 셀렉트박스
countries = sorted(df["Country"].unique())
selected_country = st.selectbox("📌 국가를 선택하세요:", countries, index=0)

# 선택한 국가의 데이터 가져오기
country_row = df[df["Country"] == selected_country].iloc[0]

# DataFrame 구성 및 비율 내림차순 정렬
country_mbti = (
    pd.DataFrame({
        "MBTI": MBTI_TYPES,
        "Ratio": [country_row[m] for m in MBTI_TYPES],
    })
    .sort_values(by="Ratio", ascending=False)
    .reset_index(drop=True)
)

# 2. 색상 로직: 1등 핑크색, 2~16등 파란색 계열 흐려지는 그라데이션
blue_shades = [
    "#003f5c",
    "#114a6b",
    "#20567a",
    "#2d6289",
    "#3a6e98",
    "#477aa8",
    "#5487b7",
    "#6193c7",
    "#6ea0d7",
    "#7bacdf",
    "#89b9eb",
    "#98c5f2",
    "#a6d2f8",
    "#b5defe",
    "#c6ebff",
]
colors = ["#FF69B4"] + blue_shades

# 3. 막대그래프 시각화
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(
    country_mbti["MBTI"],
    country_mbti["Ratio"] * 100,
    color=colors,
    edgecolor="none",
    width=0.6,
)

# 그래프 레이아웃 지정
ax.set_title(
    f"[{selected_country}] MBTI Distribution (%)",
    fontsize=15,
    pad=15,
    fontweight="bold",
)
ax.set_ylabel("Ratio (%)", fontsize=12)
ax.set_xlabel("MBTI Type", fontsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

# 막대 상단 수치 라벨 추가
for bar in bars:
  height = bar.get_height()
  ax.annotate(
      f"{height:.2f}%",
      xy=(bar.get_x() + bar.get_width() / 2, height),
      xytext=(0, 3),
      textcoords="offset points",
      ha="center",
      va="bottom",
      fontsize=9,
      fontweight="bold",
  )

ax.set_ylim(0, country_mbti["Ratio"].max() * 100 * 1.15)

st.pyplot(fig)

# 요약 정보 카드
col1, col2, col3 = st.columns(3)
col1.metric("선택 국가", selected_country)
col2.metric("1등 MBTI 유형", country_mbti.iloc[0]["MBTI"])
col3.metric("1등 점유율", f"{country_mbti.iloc[0]['Ratio']*100:.2f}%")

with st.expander("📄 전체 순위 및 비율 데이터 표 보기"):
  st.dataframe(
      country_mbti.assign(
          Percentage=lambda x: (x["Ratio"] * 100).map("{:.2f}%".format)
      ),
      use_container_width=True,
  )
