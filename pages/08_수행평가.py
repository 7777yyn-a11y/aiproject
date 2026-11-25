import folium
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Daejeon Top 10 Tourist Spots for Foreigners",
    page_icon="🗺️",
    layout="wide",
)

st.title("🗺️ 외국인이 사랑하는 대전 주요 관광지 Top 10")
st.markdown(
    "외국인 관광객에게 인기 있는 대전의 대표 명소 10곳입니다. 왼쪽 사이드바에서 카테고리를 선택해 보세요."
)

TOURIST_SPOTS = [
    {
        "rank": 1,
        "name_ko": "성심당 본점",
        "name_en": "Sungsimdang Bakery (Main)",
        "category": "미식/쇼핑",
        "lat": 36.3277,
        "lon": 127.4273,
        "desc": "1956년 개업한 대한민국 대표 베이커리. 튀김소보로와 부추빵이 유명하며 외국인 필수 방문 코스입니다.",
    },
    {
        "rank": 2,
        "name_ko": "한밭수목원",
        "name_en": "Hanbat Arboretum",
        "category": "자연/힐링",
        "lat": 36.3690,
        "lon": 127.3881,
        "desc": "전국 최대 규모의 도심 속 인공수목원으로 사계절 내내 산책과 피크닉을 즐기기 좋습니다.",
    },
    {
        "rank": 3,
        "name_ko": "유성온천 족욕체험장",
        "name_en": "Yuseong Hot Spring Foot Bath",
        "category": "체험/힐링",
        "lat": 36.3552,
        "lon": 127.3438,
        "desc": "도심 속에서 무료로 천연 온천수 족욕을 경험할 수 있는 힐링 명소입니다.",
    },
    {
        "rank": 4,
        "name_ko": "장태산 자연휴양림",
        "name_en": "Jangtaesan Recreational Forest",
        "category": "자연/힐링",
        "lat": 36.2166,
        "lon": 127.3407,
        "desc": "울창한 메타세쿼이아 숲과 스카이웨이, 출렁다리가 어우러져 이국적인 풍경을 자랑합니다.",
    },
    {
        "rank": 5,
        "name_ko": "엑스포과학공원 (한빛탑)",
        "name_en": "Expo Science Park & Hanbit Tower",
        "category": "과학/야경",
        "lat": 36.3768,
        "lon": 127.3881,
        "desc": "과학 도시 대전을 상징하는 한빛탑 전망대와 물빛광장 음악분수 야경이 인기입니다.",
    },
    {
        "rank": 6,
        "name_ko": "계족산 황톳길",
        "name_en": "Gyejoksan Red Clay Trail",
        "category": "자연/체험",
        "lat": 36.3982,
        "lon": 127.4418,
        "desc": "14.5km 구간의 부드러운 황톳길을 맨발로 걸으며 숲속 힐링을 체험할 수 있는 명소입니다.",
    },
    {
        "rank": 7,
        "name_ko": "대청호 오백리길 (명상정원)",
        "name_en": "Daecheongho Lake Trail",
        "category": "자연/힐링",
        "lat": 36.3775,
        "lon": 127.4847,
        "desc": "아름다운 호수 풍경과 수변 데크길이 조성된 트레킹 명소로 드라마 촬영지로도 유명합니다.",
    },
    {
        "rank": 8,
        "name_ko": "국립중앙과학관",
        "name_en": "National Science Museum",
        "category": "과학/문화",
        "lat": 36.3756,
        "lon": 127.3765,
        "desc": "한국의 과학기술 역사와 미래 기술을 체험형 전시로 만날 수 있는 대표 과학관입니다.",
    },
    {
        "rank": 9,
        "name_ko": "으능정이 문화의거리 (스카이로드)",
        "name_en": "Euneungjeongi Cultural Street",
        "category": "문화/쇼핑",
        "lat": 36.3291,
        "lon": 127.4285,
        "desc": "초대형 LED 아케이드 쇼와 다양한 길거리 음식, 젊은 문화를 즐길 수 있는 원도심 중심가입니다.",
    },
    {
        "rank": 10,
        "name_ko": "대동하늘공원",
        "name_en": "Daedong Sky Park",
        "category": "야경/포토존",
        "lat": 36.3340,
        "lon": 127.4485,
        "desc": "벽화마을 언덕 위 풍차와 함께 대전 시내의 노을과 야경을 한눈에 담을 수 있는 전망 명소입니다.",
    },
]

df = pd.DataFrame(TOURIST_SPOTS)

st.sidebar.header("🔍 관광지 필터")
categories = ["전체"] + sorted(df["category"].unique().tolist())
selected_category = st.sidebar.selectbox("카테고리 선택", categories)

filtered_df = (
    df[df["category"] == selected_category]
    if selected_category != "전체"
    else df
)

center_lat = float(filtered_df["lat"].mean())
center_lon = float(filtered_df["lon"].mean())

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles="OpenStreetMap",
)

color_map = {
    "미식/쇼핑": "red",
    "자연/힐링": "green",
    "체험/힐링": "lightgreen",
    "과학/야경": "blue",
    "자연/체험": "darkgreen",
    "과학/문화": "cadetblue",
    "문화/쇼핑": "orange",
    "야경/포토존": "purple",
}

for _, row in filtered_df.iterrows():
    popup_html = f"""
    <div style="width: 230px; font-family: sans-serif;">
        <h4 style="margin: 0 0 4px 0;">#{row['rank']} {row['name_ko']}</h4>
        <p style="color: #555; font-size: 12px; margin: 0 0 6px 0;">
            <b>{row['name_en']}</b> · {row['category']}
        </p>
        <p style="font-size: 12.5px; line-height: 1.4; margin: 0;">{row['desc']}</p>
    </div>
    """
    folium.Marker(
        location=[float(row["lat"]), float(row["lon"])],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=f"#{row['rank']} {row['name_ko']} ({row['name_en']})",
        icon=folium.Icon(
            color=color_map.get(row["category"], "blue"),
            icon="info-sign",
        ),
    ).add_to(m)

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📍 관광지 위치 지도")
    components.html(m._repr_html_(), height=560, scrolling=False)

with col2:
    st.subheader("📋 Top 10 리스트")
    for _, row in filtered_df.iterrows():
        with st.expander(
            f"#{row['rank']} {row['name_ko']} ({row['name_en']})",
            expanded=(row["rank"] <= 3),
        ):
            st.caption(f"카테고리: {row['category']}")
            st.write(row["desc"])
