import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
from sklearn.linear_model import LinearRegression

# --- 운영체제별 한글 폰트 설정 ---
def set_font():
    os_name = platform.system()
    if os_name == "Windows":
        plt.rc("font", family="Malgun Gothic")
    elif os_name == "Darwin":  # macOS
        plt.rc("font", family="AppleGothic")
    else:  # Linux (Streamlit Cloud 환경 등)
        # 나눔고딕 등 리눅스 환경에 설치될 수 있는 폰트 확인
        font_list = [f.name for f in fm.fontManager.ttflist]
        if "NanumGothic" in font_list:
            plt.rc("font", family="NanumGothic")
        elif "DejaVu Sans" in font_list:
            # 폰트가 없을 경우 기본 폰트로 설정하되 마이너스 기호 깨짐 방지
            pass
    # 마이너스 기호 깨짐 현상 방지
    plt.rcParams["axes.unicode_minus"] = False

set_font()

# 페이지 기본 설정
st.set_page_config(page_title="월별 평균기온 예측기", page_icon="🌡️", layout="wide")

@st.cache_data
def load_data():
    # 인코딩 자동 처리 (cp949 또는 utf-8)
    try:
        df = pd.read_csv("temperature.csv", encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv("temperature.csv", encoding="utf-8")

    # '일시' 컬럼(예: Oct-07)에서 월과 4자리 연도 추출
    df["일시"] = df["일시"].astype(str).str.strip()
    parts = df["일시"].str.split("-", expand=True)

    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    df["월"] = parts[0].map(month_map)
    yy = parts[1].astype(int)

    # 1907년 -> 1999년 -> 2000년 -> 2026년 세기 전환 처리
    years = []
    curr_century = 1900
    prev_yy = None
    for y in yy:
        if prev_yy is not None and prev_yy == 99 and y == 0:
            curr_century += 100
        years.append(curr_century + y)
        prev_yy = y

    df["연도"] = years
    # 평균기온 결측치 제거
    df = df.dropna(subset=["평균기온(℃)", "연도", "월"]).copy()
    return df

# 데이터 로드
try:
    df = load_data()
except FileNotFoundError:
    st.error("`temperature.csv` 파일을 찾을 수 없습니다. 같은 폴더에 파일을 위치시켜 주세요.")
    st.stop()

# 타이틀 영역
st.title("🌡️ 선형회귀 기반 월별 평균기온 예측 및 원리 시각화")
st.markdown("과거 기온 데이터를 바탕으로 **선형회귀(Linear Regression)** 모델이 미래 기온을 어떻게 예측하는지 시각적으로 확인해보세요.")

# 사이드바 사용자 입력
st.sidebar.header("🔍 예측 조건 설정")
selected_month = st.sidebar.selectbox("1. 예측할 월을 선택하세요", list(range(1, 13)), format_func=lambda x: f"{x}월")
min_data_year = int(df["연도"].min())
max_data_year = int(df["연도"].max())

target_year = st.sidebar.number_input(
    "2. 예측할 연도를 입력하세요",
    min_value=max_data_year + 1,
    max_value=2150,
    value=2030,
    step=1
)

# 선택한 월 데이터 필터링
month_df = df[df["월"] == selected_month].sort_values("연도")

# 선형회귀 모델 학습
X = month_df[["연도"]].values
y = month_df["평균기온(℃)"].values

model = LinearRegression()
model.fit(X, y)

# 예측 수행
pred_temp = model.predict([[target_year]])[0]
slope = model.coef_[0]          # 기울기 (1년당 기온 변화량)
intercept = model.intercept_    # y절편
y_fit = model.predict(X)        # 과거 연도에 대한 추세선 값

# 상단 핵심 지표(KPI) 표시
col1, col2, col3 = st.columns(3)
col1.metric(f"{target_year}년 {selected_month}월 예측 평균기온", f"{pred_temp:.2f} ℃")
col2.metric("10년당 평균 기온 변화 추세", f"{slope * 10:+.2f} ℃ / 10년")
col3.metric(f"역대 {selected_month}월 평균기온 ({min_data_year}~{max_data_year})", f"{y.mean():.2f} ℃")

# --- 그래프 시각화 (선형회귀 작동 원리 직관적 표현) ---
fig, ax = plt.subplots(figsize=(12, 6))

# 1. 과거 실제 기온 데이터 (산점도 + 연한 연결선)
ax.plot(month_df["연도"], y, color="lightgray", linewidth=1, zorder=1)
ax.scatter(
    month_df["연도"], y,
    color="#3b82f6", alpha=0.75, s=45, label=f"과거 실제 {selected_month}월 평균기온", zorder=3
)

# 2. 선형회귀 오차(잔차) 시각화: 실제값과 추세선 사이의 수직 점선
for idx in range(len(month_df)):
    yr = month_df["연도"].iloc[idx]
    actual = y[idx]
    fitted = y_fit[idx]
    ax.plot(
        [yr, yr], [actual, fitted],
        color="gray", linestyle=":", linewidth=0.8, alpha=0.6,
        label="오차(잔차): 실제값과 추세선의 거리" if idx == 0 else ""
    )

# 3. 학습된 선형회귀 직선 (과거 구간)
ax.plot(
    month_df["연도"], y_fit,
    color="#ef4444", linewidth=2.5,
    label=f"선형회귀 추세선 (기온 = {slope:.4f}×연도 {intercept:+.1f})", zorder=4
)

# 4. 미래 예측 구간 연장선 (마지막 데이터 연도 ~ 목표 연도)
last_year = month_df["연도"].max()
future_years = np.array([[last_year], [target_year]])
future_preds = model.predict(future_years)
ax.plot(
    future_years.flatten(), future_preds,
    color="#ef4444", linestyle="--", linewidth=2.5,
    label="미래 추세 연장선 (예측 경로)", zorder=4
)

# 5. 최종 예측 지점 강조 및 수직/수평 보조선
ax.scatter(
    [target_year], [pred_temp],
    color="#f59e0b", edgecolor="black", s=220, marker="*", zorder=6,
    label=f"{target_year}년 예측 기온 ({pred_temp:.2f}℃)"
)
ax.axvline(x=target_year, color="#f59e0b", linestyle=":", alpha=0.7)
ax.axhline(y=pred_temp, color="#f59e0b", linestyle=":", alpha=0.7)

# 예측값 텍스트 주석
ax.annotate(
    f"  {target_year}년 {selected_month}월 예측\n  ▶ {pred_temp:.2f}℃",
    xy=(target_year, pred_temp),
    xytext=(target_year - (target_year - min_data_year) * 0.18, pred_temp + (y.max() - y.min()) * 0.12),
    fontsize=11, fontweight="bold", color="#b45309",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#fef3c7", edgecolor="#f59e0b", lw=1.5),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.15", color="#b45309", lw=1.5),
    zorder=7
)

# 그래프 스타일링
ax.set_title(f"[{min_data_year}~{max_data_year}] {selected_month}월 평균기온 변화 및 {target_year}년 선형회귀 예측", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("연도 (Year)", fontsize=12)
ax.set_ylabel("평균기온 (℃)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.9, fontsize=10)

st.pyplot(fig)

# --- 그래프 하단: 선형회귀 알고리즘 쉬운 설명 ---
st.divider()
st.subheader("💡 그래프 속 '선형회귀(Linear Regression)' 알고리즘은 어떻게 작동할까요?")

st.markdown(f"""
선형회귀는 복잡하게 오르내리는 과거 데이터 속에서 **가장 대표적인 하나의 직선(추세선)**을 찾아 미래를 예측하는 머신러닝 알고리즘입니다. 위 그래프를 3단계로 따라가 보면 원리를 쉽게 이해할 수 있습니다.

1. **과거 데이터 찍기 (파란색 점)**  
   먼저 {min_data_year}년부터 {max_data_year}년까지 기록된 역대 **{selected_month}월의 평균기온**을 좌표평면 위에 점으로 찍습니다. 해마다 날씨 변동 때문에 점들이 위아래로 흩어져 있습니다.
2. **오차가 가장 적은 최적의 직선 찾기 (빨간색 실선 & 회색 점선)**  
   컴퓨터는 모든 파란색 점들의 한가운데를 관통하는 직선을 긋습니다. 이때 각 점(실제 기온)과 직선 사이의 세로 거리인 **'오차(회색 점선)'들의 제곱 합이 최소가 되는 단 하나의 직선**을 수학적으로 계산해 냅니다.  
   * 현재 {selected_month}월 데이터에서 찾은 직선의 기울기는 **{slope:+.4f}**입니다. 즉, 매년 평균적으로 **{slope:+.4f}℃**씩(10년이면 **{slope*10:+.2f}℃**) 변하는 추세를 보입니다.
3. **직선을 미래로 연장하여 예측하기 (빨간색 점선 & 노란색 별)**  
   과거의 추세가 앞으로도 일정하게 이어진다고 가정하고, 빨간색 직선을 사용자가 입력한 **{target_year}년**까지 그대로 쭉 연장합니다. 그 연장선이 {target_year}년과 만나는 지점(노란색 별)의 높이를 읽은 값이 바로 예측 기온인 **{pred_temp:.2f}℃**입니다.
""")

# 데이터 표 확인 옵션
with st.expander(f"📊 {selected_month}월 과거 기온 원본 데이터 보기"):
    st.dataframe(month_df[["연도", "월", "평균기온(℃)", "평균최고기온(℃)", "평균최저기온(℃)"]].reset_index(drop=True), use_container_width=True)
