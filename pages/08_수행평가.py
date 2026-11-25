import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 기본 설정
st.set_page_config(
    page_title="Top 10 Daejeon Attractions for Foreigners",
    page_icon="🗺️",
    layout="wide"
)

# 외국인 선호 대전 주요 관광지 Top 10 데이터 (한국관광공사 및 대전관광 데이터 기반)
ATTRACTIONS = [
    {
        "rank": 1,
        "name_ko": "성심당 본점",
        "name_en": "Sungsimdang Main Store",
        "category": "미식 (Food)",
        "lat": 36.3276,
        "lon": 127.4273,
        "desc_en": "Daejeon's iconic bakery founded in 1956, famous for Fried Soboro bread.",
        "desc_ko": "1956년 개업한 대전의 대표 향토 제과점. 튀김소보로와 부추빵으로 유명한 미식 성지."
    },
    {
        "rank": 2,
        "name_ko": "한밭수목원",
        "name_en": "Hanbat Arboretum",
        "category": "자연/힐링 (Nature)",
        "lat": 36.3698,
        "lon": 127.3882,
        "desc_en": "The largest man-made urban arboretum in Korea, ideal for a relaxing stroll.",
        "desc_ko": "전국 최대 규모의 도심 속 인공수목원. 열대식물원과 산책로가 잘 조성되어 있음."
    },
    {
        "rank": 3,
        "name_ko": "장태산자연휴양림",
        "name_en": "Jangtaesan Natural Recreation Forest",
        "category": "자연/힐링 (Nature)",
        "lat": 36.2160,
        "lon": 127.3413,
        "desc_en": "Exotic dense Metasequoia forest featuring a thrilling skyway bridge.",
        "desc_ko": "국내 유일의 메타세쿼이아 숲이 울창하게 형성된 휴양림으로 스카이웨이 전망대가 인기."
    },
    {
        "rank": 4,
        "name_ko": "유성온천 족욕체험장",
        "name_en": "Yuseong Hot Springs Foot Bath",
        "category": "체험/휴양 (Experience)",
        "lat": 36.3551,
        "lon": 127.3446,
        "desc_en": "Free outdoor natural hot spring foot spa open year-round in the city.",
        "desc_ko": "100% 천연 온천수를 연중무휴 무료로 즐길 수 있는 도심 속 노천 족욕 명소."
    },
    {
        "rank": 5,
        "name_ko": "엑스포과학공원 (한빛탑)",
        "name_en": "Expo Science Park (Hanbit Tower)",
        "category": "과학/야경 (Landmark)",
        "lat": 36.3766,
        "lon": 127.3872,
        "desc_en": "Symbol of Daejeon's science identity with musical fountains and night views.",
        "desc_ko": "93 대전엑스포의 상징. 한빛탑 전망대와 물빛광장 음악분수 야경이 돋보이는 곳."
    },
    {
        "rank": 6,
        "name_ko": "계족산 황톳길",
        "name_en": "Gyejoksan Red Clay Trail",
        "category": "체험/휴양 (Experience)",
        "lat": 36.4041,
        "lon": 127.4298,
        "desc_en": "14.5km barefoot forest walking trail covered in soft red clay.",
        "desc_ko": "14.5km 숲속 임도에 황토를 깔아 맨발 걷기와 산림욕을 동시에 즐기는 힐링 코스."
    },
    {
        "rank": 7,
        "name_ko": "대청호 오백리길 (4구간)",
        "name_en": "Daecheongho Lake 500-ri Trail",
        "category": "자연/힐링 (Nature)",
        "lat": 36.4098,
        "lon": 127.4986,
        "desc_en": "Scenic lakeside walking course famous for reed fields and filming locations.",
        "desc_ko": "호수와 산이 어우러진 수변 산책길. 갈대밭과 드라마 촬영지로 외국인에게 인기가 높음."
    },
    {
        "rank": 8,
        "name_ko": "우암사적공원",
        "name_en": "Uam Historic Park",
        "category": "역사/전통 (History)",
        "lat": 36.3364,
        "lon": 127.4564,
        "desc_en": "Traditional Joseon-era Confucian academy architecture and serene pond.",
        "desc_ko": "조선 후기 대학자 송시열 선생이 학문을 닦던 곳으로 고즈넉한 한옥과 연못 풍경이 일품."
    },
    {
        "rank": 9,
        "name_ko": "대동하늘공원",
        "name_en": "Daedong Sky Park",
        "category": "과학/야경 (Landmark)",
        "lat": 36.3292,
        "lon": 127.4485,
        "desc_en": "Hilltop mural village offering panoramic sunset and city night views.",
        "desc_ko": "벽화마을 언덕 정상의 풍차 전망대에서 대전 도심의 일몰과 야경을 한눈에 담는 명소."
    },
    {
        "rank": 10,
        "name_ko": "으능정이 문화의거리",
        "name_en": "Euneungjeongi Culture Street",
        "category": "미식 (Food)",
        "lat": 36.3284,
        "lon": 127.4278,
        "desc_en": "Vibrant youth street featuring the giant LED Skyroad and local eateries.",
        "desc_ko": "대형 LED 아케이드 스카이로드와 다양한 먹거리, 쇼핑이 어우러진 대전 원도심 중심가."
    }
]

# 카테고리별 마커 색상 지정
CATEGORY_COLORS = {
    "미식 (Food)": "red",
    "자연/힐링 (Nature)": "green",
    "체험/휴양 (Experience)": "orange",
    "과학/야경 (Landmark)": "purple",
    "역사/전통 (History)": "blue"
}

# 타이틀 영역
st.title("🇰🇷 외국인이 사랑하는 대전 주요 관광지 Top 10")
st.markdown("Top 10 Must-Visit Tourist Attractions in **Daejeon** for International Visitors")

# 사이드바 필터 및 선택 컨트롤
with st.sidebar:
    st.header("🔍 탐색 필터 (Filter)")
    
    all_categories = list(CATEGORY_COLORS.keys())
    selected_categories = st.multiselect(
        "테마별 보기 (Category)",
        options=all_categories,
        default=all_categories
    )
    
    filtered_places = [p for p in ATTRACTIONS if p["category"] in selected_categories]
    
    st.divider()
    st.subheader("📍 명소 바로가기 (Quick Focus)")
    place_options = ["전체 보기 (All Top 10)"] + [
        f"#{p['rank']} {p['name_ko']} ({p['name_en']})" for p in filtered_places
    ]
    selected_place_label = st.selectbox("지도 중심 이동:", place_options)

# 지도 중심 좌표 및 줌 레벨 결정
if selected_place_label == "전체 보기 (All Top 10)" or not filtered_places:
    center_lat, center_lon = 36.3504, 127.3845  # 대전 시청 기준 중심 좌표
    zoom_level = 11
    focused_rank = None
else:
    focused_rank = int(selected_place_label.split()[0].replace("#", ""))
    target = next(p for p in filtered_places if p["rank"] == focused_rank)
    center_lat, center_lon = target["lat"], target["lon"]
    zoom_level = 15

# Folium 지도 생성
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=zoom_level,
    tiles="CartoDB positron"
)

# 마커 추가
for place in filtered_places:
    color = CATEGORY_COLORS.get(place["category"], "blue")
    
    popup_html = f"""
    <div style="width: 240px; font-family: sans-serif; line-height: 1.4;">
        <span style="background-color: #f0f2f6; padding: 2px 6px; border-radius: 4px; font-size: 11px;">
            {place['category']}
        </span>
        <h4 style="margin: 6px 0 2px 0;">#{place['rank']} {place['name_ko']}</h4>
        <div style="color: #555; font-size: 12px; font-weight: bold; margin-bottom: 6px;">
            {place['name_en']}
        </div>
        <p style="font-size: 12px; margin: 0 0 6px 0; color: #222;">{place['desc_en']}</p>
        <p style="font-size: 11px; margin: 0; color: #666;">{place['desc_ko']}</p>
    </div>
    """
    
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=folium.Popup(popup_html, max_width=260),
        tooltip=f"#{place['rank']} {place['name_ko']} ({place['name_en']})",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

# 레이아웃 분할 (좌측 지도 / 우측 리스트)
col1, col2 = st.columns([2.2, 1])

with col1:
    st_folium(m, width="100%", height=620, returned_objects=[])

with col2:
    st.subheader("📋 선정 명소 리스트")
    if not filtered_places:
        st.warning("선택된 카테고리가 없습니다. 사이드바에서 테마를 선택해주세요.")
    else:
        for p in filtered_places:
            with st.expander(f"#{p['rank']} {p['name_ko']} | {p['name_en']}", expanded=(p["rank"] == focused_rank)):
                st.caption(f"카테고리: {p['category']}")
                st.write(f"**EN:** {p['desc_en']}")
                st.write(f"**KO:** {p['desc_ko']}")
