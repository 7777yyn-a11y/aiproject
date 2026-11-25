import math
import folium
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Daejeon Top 10 & Travel Planner",
    page_icon="🗺️",
    layout="wide",
)

st.title("🗺️ 외국인이 사랑하는 대전 관광지 Top 10 & 맞춤 여행 플래너")
st.markdown(
    "대전의 대표 명소 10곳을 지도로 둘러보고, 일정과 취향에 맞춘 최적 동선 여행 코스를 자동으로 만들어보세요."
)

TOURIST_SPOTS = [
    {
        "rank": 1,
        "name_ko": "성심당 본점",
        "name_en": "Sungsimdang Bakery (Main)",
        "category": "미식/쇼핑",
        "area": "원도심(중구)",
        "stay_min": 60,
        "best_time": "오전/오후",
        "lat": 36.3277,
        "lon": 127.4273,
        "desc": "1956년 개업한 대한민국 대표 베이커리. 튀김소보로와 부추빵이 유명하며 외국인 필수 방문 코스입니다.",
    },
    {
        "rank": 2,
        "name_ko": "한밭수목원",
        "name_en": "Hanbat Arboretum",
        "category": "자연/힐링",
        "area": "둔산권(서구)",
        "stay_min": 90,
        "best_time": "오전/오후",
        "lat": 36.3690,
        "lon": 127.3881,
        "desc": "전국 최대 규모의 도심 속 인공수목원으로 사계절 내내 산책과 피크닉을 즐기기 좋습니다.",
    },
    {
        "rank": 3,
        "name_ko": "유성온천 족욕체험장",
        "name_en": "Yuseong Hot Spring Foot Bath",
        "category": "체험/힐링",
        "area": "유성권(유성구)",
        "stay_min": 50,
        "best_time": "오후/저녁",
        "lat": 36.3552,
        "lon": 127.3438,
        "desc": "도심 속에서 무료로 천연 온천수 족욕을 경험할 수 있는 힐링 명소입니다.",
    },
    {
        "rank": 4,
        "name_ko": "장태산 자연휴양림",
        "name_en": "Jangtaesan Recreational Forest",
        "category": "자연/힐링",
        "area": "외곽남부(서구)",
        "stay_min": 120,
        "best_time": "오전/오후",
        "lat": 36.2166,
        "lon": 127.3407,
        "desc": "울창한 메타세쿼이아 숲과 스카이웨이, 출렁다리가 어우러져 이국적인 풍경을 자랑합니다.",
    },
    {
        "rank": 5,
        "name_ko": "엑스포과학공원 (한빛탑)",
        "name_en": "Expo Science Park & Hanbit Tower",
        "category": "과학/야경",
        "area": "유성권(유성구)",
        "stay_min": 90,
        "best_time": "저녁/야경",
        "lat": 36.3768,
        "lon": 127.3881,
        "desc": "과학 도시 대전을 상징하는 한빛탑 전망대와 물빛광장 음악분수 야경이 인기입니다.",
    },
    {
        "rank": 6,
        "name_ko": "계족산 황톳길",
        "name_en": "Gyejoksan Red Clay Trail",
        "category": "자연/체험",
        "area": "외곽북동부(대덕구)",
        "stay_min": 120,
        "best_time": "오전",
        "lat": 36.3982,
        "lon": 127.4418,
        "desc": "14.5km 구간의 부드러운 황톳길을 맨발로 걸으며 숲속 힐링을 체험할 수 있는 명소입니다.",
    },
    {
        "rank": 7,
        "name_ko": "대청호 오백리길 (명상정원)",
        "name_en": "Daecheongho Lake Trail",
        "category": "자연/힐링",
        "area": "외곽동부(동구)",
        "stay_min": 110,
        "best_time": "오후",
        "lat": 36.3775,
        "lon": 127.4847,
        "desc": "아름다운 호수 풍경과 수변 데크길이 조성된 트레킹 명소로 드라마 촬영지로도 유명합니다.",
    },
    {
        "rank": 8,
        "name_ko": "국립중앙과학관",
        "name_en": "National Science Museum",
        "category": "과학/문화",
        "area": "유성권(유성구)",
        "stay_min": 100,
        "best_time": "오전/오후",
        "lat": 36.3756,
        "lon": 127.3765,
        "desc": "한국의 과학기술 역사와 미래 기술을 체험형 전시로 만날 수 있는 대표 과학관입니다.",
    },
    {
        "rank": 9,
        "name_ko": "으능정이 문화의거리 (스카이로드)",
        "name_en": "Euneungjeongi Cultural Street",
        "category": "문화/쇼핑",
        "area": "원도심(중구)",
        "stay_min": 80,
        "best_time": "오후/저녁",
        "lat": 36.3291,
        "lon": 127.4285,
        "desc": "초대형 LED 아케이드 쇼와 다양한 길거리 음식, 젊은 문화를 즐길 수 있는 원도심 중심가입니다.",
    },
    {
        "rank": 10,
        "name_ko": "대동하늘공원",
        "name_en": "Daedong Sky Park",
        "category": "야경/포토존",
        "area": "원도심(동구)",
        "stay_min": 60,
        "best_time": "저녁/야경",
        "lat": 36.3340,
        "lon": 127.4485,
        "desc": "벽화마을 언덕 위 풍차와 함께 대전 시내의 노을과 야경을 한눈에 담을 수 있는 전망 명소입니다.",
    },
]

df = pd.DataFrame(TOURIST_SPOTS)


def calc_distance_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def optimize_route(spots_list):
    if not spots_list:
        return []
    remaining = spots_list.copy()
    # 첫 번째 방문지는 인기도(rank)가 가장 높은 곳으로 시작
    remaining.sort(key=lambda x: x["rank"])
    ordered = [remaining.pop(0)]
    while remaining:
        last = ordered[-1]
        remaining.sort(
            key=lambda x: calc_distance_km(last["lat"], last["lon"], x["lat"], x["lon"])
        )
        ordered.append(remaining.pop(0))
    return ordered


tab1, tab2 = st.tabs(["📍 Top 10 관광지 지도", "🗓️ AI 맞춤 대전 여행 플래너"])

# ==========================================
# TAB 1: 기존 Top 10 지도 탐색
# ==========================================
with tab1:
    st.subheader("카테고리별 인기 명소 탐색")
    categories = ["전체"] + sorted(df["category"].unique().tolist())
    selected_category = st.selectbox("카테고리 필터", categories, key="map_filter")

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
        components.html(m._repr_html_(), height=560, scrolling=False)

    with col2:
        st.markdown("#### 📋 명소 상세 리스트")
        for _, row in filtered_df.iterrows():
            with st.expander(
                f"#{row['rank']} {row['name_ko']} ({row['name_en']})",
                expanded=(row["rank"] <= 3),
            ):
                st.caption(f"카테고리: {row['category']} | 권역: {row['area']} | 권장 체류: {row['stay_min']}분")
                st.write(row["desc"])


# ==========================================
# TAB 2: 맞춤형 대전 여행 플래너
# ==========================================
with tab2:
    st.subheader("나만의 대전 여행 코스 만들기")
    st.markdown("원하는 조건을 선택하면 이동 거리를 최소화한 추천 일정과 동선 지도를 만들어 드립니다.")

    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        duration = st.selectbox(
            "여행 기간",
            ["당일치기 (1일)", "1박 2일 (2일)", "2박 3일 (3일)"],
        )
    with p_col2:
        themes = st.multiselect(
            "선호 테마 (복수 선택)",
            ["미식/쇼핑", "자연/힐링", "과학/문화", "야경/감성"],
            default=["미식/쇼핑", "자연/힐링", "야경/감성"],
        )
    with p_col3:
        transport = st.selectbox(
            "주요 이동 수단",
            ["대중교통 / 도보", "자차 / 택시"],
        )
    with p_col4:
        pace = st.selectbox(
            "여행 템포",
            ["여유롭게 (하루 3곳)", "알차게 (하루 4곳)"],
        )

    days_map = {"당일치기 (1일)": 1, "1박 2일 (2일)": 2, "2박 3일 (3일)": 3}
    num_days = days_map[duration]
    spots_per_day = 3 if "3곳" in pace else 4
    total_needed = min(num_days * spots_per_day, len(TOURIST_SPOTS))

    # 테마 매핑
    theme_to_cat = {
        "미식/쇼핑": ["미식/쇼핑", "문화/쇼핑"],
        "자연/힐링": ["자연/힐링", "체험/힐링", "자연/체험"],
        "과학/문화": ["과학/야경", "과학/문화"],
        "야경/감성": ["과학/야경", "야경/포토존"],
    }

    preferred_cats = set()
    for t in themes:
        preferred_cats.update(theme_to_cat.get(t, []))

    # 우선순위 점수 계산 (선호 테마 가중치 + 대중교통일 경우 도심권 가산점 + 인기도)
    scored_spots = []
    for spot in TOURIST_SPOTS:
        score = 20 - spot["rank"]  # 기본 인기도 점수
        if spot["category"] in preferred_cats:
            score += 15
        if transport == "대중교통 / 도보" and "외곽" not in spot["area"]:
            score += 8
        scored_spots.append((score, spot))

    scored_spots.sort(key=lambda x: x[0], reverse=True)
    selected_spots = [item[1] for item in scored_spots[:total_needed]]

    # 동선 최적화 후 일차별 배분
    optimized_spots = optimize_route(selected_spots)
    day_plans = []
    for d in range(num_days):
        start_idx = d * spots_per_day
        end_idx = start_idx + spots_per_day
        day_slice = optimized_spots[start_idx:end_idx]
        if day_slice:
            # 야경/저녁 명소가 있다면 해당 일차의 마지막으로 배치
            day_slice.sort(key=lambda x: 1 if "야경" in x["best_time"] or "저녁" in x["best_time"] else 0)
            day_plans.append(day_slice)

    st.divider()

    res_col1, res_col2 = st.columns([1.2, 1])

    with res_col1:
        st.markdown("### 📅 추천 상세 일정표")
        start_hours = [10, 13, 16, 19]
        plan_text_lines = [f"[대전 {duration} 맞춤 여행 코스 - {transport}]"]

        for day_idx, spots in enumerate(day_plans, start=1):
            st.markdown(f"#### Day {day_idx}")
            plan_text_lines.append(f"\n=== Day {day_idx} ===")
            table_rows = []
            for idx, s in enumerate(spots):
                hour = start_hours[idx] if idx < len(start_hours) else 19
                time_str = f"{hour:02d}:00"
                dist_info = "-"
                if idx > 0:
                    prev = spots[idx - 1]
                    km = calc_distance_km(prev["lat"], prev["lon"], s["lat"], s["lon"])
                    est_min = int(km * (4 if transport == "대중교통 / 도보" else 2.5) + 10)
                    dist_info = f"약 {km:.1f}km (약 {est_min}분)"

                table_rows.append(
                    {
                        "순서": f"{day_idx}-{idx+1}",
                        "시작 시간": time_str,
                        "관광지": f"{s['name_ko']} ({s['name_en']})",
                        "테마": s["category"],
                        "권장 체류": f"{s['stay_min']}분",
                        "이전 장소에서 이동": dist_info,
                    }
                )
                plan_text_lines.append(
                    f"{time_str} | {s['name_ko']} ({s['category']}) - 권장 {s['stay_min']}분 | 이동: {dist_info}"
                )

            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

        # 일정 텍스트 다운로드 버튼
        st.download_button(
            label="📥 여행 일정표 텍스트(.txt)로 저장하기",
            data="\n".join(plan_text_lines),
            file_name="daejeon_travel_plan.txt",
            mime="text/plain",
        )

    with res_col2:
        st.markdown("### 🧭 일차별 이동 동선 지도")
        plan_map = folium.Map(
            location=[36.3504, 127.3845],
            zoom_start=11,
            tiles="OpenStreetMap",
        )

        day_colors = ["#E63946", "#1D3557", "#2A9D8F"]
        marker_colors = ["red", "darkblue", "green"]

        for day_idx, spots in enumerate(day_plans):
            line_coords = []
            color_hex = day_colors[day_idx % len(day_colors)]
            m_color = marker_colors[day_idx % len(marker_colors)]

            for idx, s in enumerate(spots):
                coord = [float(s["lat"]), float(s["lon"])]
                line_coords.append(coord)

                popup_html = f"""
                <div style="width: 210px; font-family: sans-serif;">
                    <span style="background:{color_hex}; color:white; padding:2px 6px; border-radius:4px; font-size:11px;">
                        Day {day_idx+1} - {idx+1}번째 코스
                    </span>
                    <h4 style="margin: 6px 0 4px 0;">{s['name_ko']}</h4>
                    <p style="font-size: 12px; color:#555; margin:0;">{s['category']} · 권장 {s['stay_min']}분</p>
                </div>
                """
                folium.Marker(
                    location=coord,
                    popup=folium.Popup(popup_html, max_width=230),
                    tooltip=f"[Day {day_idx+1}-{idx+1}] {s['name_ko']}",
                    icon=folium.Icon(color=m_color, icon="flag"),
                ).add_to(plan_map)

            if len(line_coords) > 1:
                folium.PolyLine(
                    locations=line_coords,
                    color=color_hex,
                    weight=4,
                    opacity=0.85,
                    dash_array="5, 5" if day_idx > 0 else None,
                    tooltip=f"Day {day_idx+1} 이동 경로",
                ).add_to(plan_map)

        components.html(plan_map._repr_html_(), height=540, scrolling=False)
        st.caption("🔴 빨간선: Day 1 경로 | 🔵 파란선: Day 2 경로 | 🟢 초록선: Day 3 경로")
