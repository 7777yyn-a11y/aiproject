import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# Page config
st.set_page_config(
    page_title="외국인 선호 서울 주요 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 외국인이 좋아하는 서울 주요 관광지 TOP 10")
st.write("서울 지도 위 마커를 클릭하거나, 아래 설명 카드 및 데이터표를 통해 각 관광지의 특징을 확인해보세요!")

# Data definition
locations = [
    {
        "rank": 1,
        "name": "경복궁",
        "category": "역사 / 문화",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선시대 대표 궁궐로 한복 체험과 왕궁 수문장 교대식이 외국인에게 매우 인기 있습니다."
    },
    {
        "rank": 2,
        "name": "N서울타워 (남산타워)",
        "category": "랜드마크 / 야경",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울 도심 전경을 한눈에 감상할 수 있는 대표 야경 스팟 및 사랑의 자물쇠 명소입니다."
    },
    {
        "rank": 3,
        "name": "명동 쇼핑거리",
        "category": "쇼핑 / 길거리 음식",
        "lat": 37.5636,
        "lon": 126.9822,
        "desc": "K-뷰티 쇼핑과 풍부한 K-길거리 음식을 즐길 수 있는 필수 방문지입니다."
    },
    {
        "rank": 4,
        "name": "북촌한옥마을",
        "category": "전통 / 거리",
        "lat": 37.5826,
        "lon": 126.9831,
        "desc": "실제 한옥들이 보존된 고즈넉한 마을로 전통적인 풍경을 사진에 담기 좋습니다."
    },
    {
        "rank": 5,
        "name": "홍대 거리",
        "category": "청춘 / 문화 / 야간",
        "lat": 37.5563,
        "lon": 126.9226,
        "desc": "버스킹, 독특한 카페, 활기찬 야간 문화와 인디 예술을 경험할 수 있는 곳입니다."
    },
    {
        "rank": 6,
        "name": "동대문디자인플라자 (DDP)",
        "category": "건축 / 쇼핑",
        "lat": 37.5665,
        "lon": 127.0090,
        "desc": "독특한 곡선 건축미와 패션 행사, 야경이 인상적인 현대 디자인 랜드마크입니다."
    },
    {
        "rank": 7,
        "name": "롯데월드타워 & 서울스카이",
        "category": "전망대 / 쇼핑",
        "lat": 37.5126,
        "lon": 127.1025,
        "desc": "세계 6위 높이의 마천루로 파노라마 한강 뷰를 자랑하는 대표 현대적 명소입니다."
    },
    {
        "rank": 8,
        "name": "인사동",
        "category": "전통 공예 / 찻집",
        "lat": 37.5743,
        "lon": 126.9897,
        "desc": "한국 전통 공예품, 갤러리, 전통 찻집 및 쌈지길이 위치한 문화 거리입니다."
    },
    {
        "rank": 9,
        "name": "이태원",
        "category": "다문화 / 미식",
        "lat": 37.5345,
        "lon": 126.9942,
        "desc": "전 세계의 음식과 다채로운 국제적 분위기를 지닌 다문화 거리입니다."
    },
    {
        "rank": 10,
        "name": "반포 한강공원",
        "category": "휴식 / 야경",
        "lat": 37.5102,
        "lon": 126.9960,
        "desc": "달빛무지개분수와 함께 한강 라면, 피크닉을 체험하는 로컬 휴식처입니다."
    }
]

df = pd.DataFrame(locations)

# 1. Map Display Section
st.subheader("📍 서울 관광지 지도 (TOP 10)")

# Initialize Folium Map centered on Seoul
m = folium.Map(location=[37.555, 126.985], zoom_start=12, tiles="OpenStreetMap")

# Add markers for each location
for idx, row in df.iterrows():
    popup_html = f"""
    <div style='width: 220px; font-family: sans-serif;'>
        <h4 style='margin-bottom: 5px;'><b>{row['rank']}. {row['name']}</b></h4>
        <p style='margin: 3px 0;'><b>카테고리:</b> {row['category']}</p>
        <p style='font-size: 13px; color: #555;'>{row['desc']}</p>
    </div>
    """
    
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=260),
        tooltip=f"{row['rank']}위: {row['name']}",
        icon=folium.Icon(color="red", icon="star", prefix="fa")
    ).add_to(m)

# Render Folium map in Streamlit
st_folium(m, width="100%", height=500)

st.markdown("---")

# 2. Information Section below the Map
st.subheader("ℹ️ TOP 10 관광지 상세 설명")

# Grid layout for cards below map
cols = st.columns(2)
for idx, row in df.iterrows():
    col = cols[idx % 2]
    with col:
        with st.expander(f"**{row['rank']}위. {row['name']}** ({row['category']})", expanded=True):
            st.write(row['desc'])

st.markdown("---")

# Summary Table
st.subheader("📊 한눈에 보는 데이터")
st.dataframe(
    df[['rank', 'name', 'category', 'desc']],
    column_config={
        "rank": "순위",
        "name": "관광지명",
        "category": "카테고리",
        "desc": "주요 특징 및 설명"
    },
    hide_index=True,
    use_container_width=True
)
