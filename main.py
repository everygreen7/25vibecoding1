import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import json
import time
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(layout="wide", page_title="디지털 칠판")

# --- 타이머 기능 ---
st.sidebar.header("타이머 설정")

# 세션 상태 초기화
if 'timer_state' not in st.session_state:
    st.session_state.timer_state = 'stopped' # 'stopped', 'running', 'paused', 'finished'
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'pause_time' not in st.session_state:
    st.session_state.pause_time = None
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0
if 'time_left' not in st.session_state:
    st.session_state.time_left = 0
if 'input_minutes' not in st.session_state:
    st.session_state.input_minutes = 0
if 'input_seconds' not in st.session_state:
    st.session_state.input_seconds = 0

# 시간 입력
col_min, col_sec = st.sidebar.columns(2)
with col_min:
    minutes = st.number_input("분", min_value=0, max_value=59, value=st.session_state.input_minutes, key="min_input")
with col_sec:
    seconds = st.number_input("초", min_value=0, max_value=59, value=st.session_state.input_seconds, key="sec_input")

# 입력 값 업데이트 (세션 상태에 저장하여 새로고침 시 유지)
st.session_state.input_minutes = minutes
st.session_state.input_seconds = seconds

# 총 시간 계산
initial_total_seconds = minutes * 60 + seconds

# 타이머 상태 업데이트 함수
def update_timer_state(state):
    st.session_state.timer_state = state
    if state == 'running':
        if st.session_state.pause_time is not None: # 일시정지 후 재개
            paused_duration = datetime.now() - st.session_state.pause_time
            st.session_state.start_time += paused_duration # 시작 시간을 일시정지 시간만큼 미룸
            st.session_state.pause_time = None
        elif st.session_state.start_time is None: # 처음 시작
             st.session_state.start_time = datetime.now()
             st.session_state.total_seconds = initial_total_seconds # 시작 시 총 시간 저장
             st.session_state.time_left = st.session_state.total_seconds
    elif state == 'paused':
        st.session_state.pause_time = datetime.now()
    elif state == 'stopped':
        st.session_state.start_time = None
        st.session_state.pause_time = None
        st.session_state.total_seconds = 0
        st.session_state.time_left = 0
        st.session_state.input_minutes = 0
        st.session_state.input_seconds = 0
    elif state == 'finished':
        st.session_state.start_time = None
        st.session_state.pause_time = None
        st.session_state.total_seconds = 0
        st.session_state.time_left = 0


# 타이머 제어 버튼
col_start, col_pause, col_reset = st.sidebar.columns(3)

with col_start:
    if st.button("시작", disabled=st.session_state.timer_state == 'running' or initial_total_seconds == 0):
        update_timer_state('running')
        st.rerun() # 상태 변경 후 새로고침하여 타이머 표시 업데이트

with col_pause:
    if st.button("일시정지", disabled=st.session_state.timer_state != 'running'):
        update_timer_state('paused')
        st.rerun() # 상태 변경 후 새로고침

with col_reset:
    if st.button("재설정", disabled=st.session_state.timer_state == 'stopped'):
        update_timer_state('stopped')
        st.rerun() # 상태 변경 후 새로고침

# 타이머 표시 영역 (메인 화면)
timer_display_area = st.empty()

# 타이머 로직 및 표시
if st.session_state.timer_state == 'running':
    elapsed_time = datetime.now() - st.session_state.start_time
    st.session_state.time_left = max(0, st.session_state.total_seconds - int(elapsed_time.total_seconds()))

    if st.session_state.time_left > 0:
        mins, secs = divmod(st.session_state.time_left, 60)
        timer_display_area.markdown(f"<h1 style='text-align: center; color: green;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
        # 1초마다 새로고침 (실시간 카운트다운처럼 보이게 함)
        time.sleep(1)
        st.rerun()
    else:
        update_timer_state('finished')
        timer_display_area.markdown("<h1 style='text-align: center; color: red;'>시간 종료!</h1>", unsafe_allow_html=True)
        st.balloons() # 시간 종료 시 알림 효과
elif st.session_state.timer_state == 'paused':
    mins, secs = divmod(st.session_state.time_left, 60)
    timer_display_area.markdown(f"<h1 style='text-align: center; color: orange;'>{mins:02d}:{secs:02d} (일시정지)</h1>", unsafe_allow_html=True)
elif st.session_state.timer_state == 'finished':
     timer_display_area.markdown("<h1 style='text-align: center; color: red;'>시간 종료!</h1>", unsafe_allow_html=True)
else: # stopped
    mins, secs = divmod(initial_total_seconds, 60)
    timer_display_area.markdown(f"<h1 style='text-align: center; color: gray;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)


st.markdown("---") # 구분선

# --- 디지털 칠판 기능 ---
st.header("디지털 칠판")

# 캔버스 설정
canvas_width = 800
canvas_height = 600

# 그리기 모드 및 색상, 두께 설정 (사이드바)
st.sidebar.header("칠판 설정")
drawing_mode = st.sidebar.selectbox(
    "그리기 모드", ("freedraw", "line", "rect", "circle", "transform", "polygon", "point", "text"), index=0
)
stroke_width = st.sidebar.slider("펜 두께", 1, 25, 3)
stroke_color = st.sidebar.color_picker("펜 색상", "#000000")
bg_color = st.sidebar.color_picker("배경 색상", "#FFFFFF")
# bg_image = st.sidebar.file_uploader("배경 이미지 업로드", type=["png", "jpg"]) # 배경 이미지 기능 (선택 사항)

# 캔버스 컴포넌트
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)", # 채우기 색상 (도형용)
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    # background_image=bg_image, # 배경 이미지 설정
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    point_display_mode="auto",
    key="canvas",
)

# 그린 내용 지우기
if st.button("모두 지우기"):
    # 캔버스 상태를 초기화하는 간단한 방법은 페이지 새로고침입니다.
    # 더 나은 방법은 캔버스 컴포넌트의 key를 변경하여 강제로 리렌더링하는 것입니다.
    st.session_state["canvas"] = st.session_state["canvas"] + 1 # key 값을 변경
    st.rerun() # 페이지 새로고침

# 그린 내용 저장 및 불러오기
st.sidebar.header("저장/불러오기")

# 그린 내용 (JSON 데이터) 가져오기
if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"])
    # st.subheader("그린 내용 (JSON 데이터)")
    # st.write(objects) # 디버깅용

    # JSON 파일로 저장
    canvas_json_data = json.dumps(canvas_result.json_data)
    st.sidebar.download_button(
        label="그린 내용 JSON으로 저장",
        data=canvas_json_data,
        file_name="digital_whiteboard.json",
        mime="application/json"
    )

# JSON 파일 불러오기
uploaded_file = st.sidebar.file_uploader("그린 내용 JSON 불러오기", type=["json"])
if uploaded_file is not None:
    loaded_json_data = json.load(uploaded_file)
    # 불러온 데이터를 캔버스에 적용하는 기능은 streamlit-drawable-canvas 컴포넌트 자체에서 지원해야 합니다.
    # 현재 버전(또는 사용 방식)에서는 직접 로드된 JSON 데이터를 캔버스에 주입하는 기능이 제한적일 수 있습니다.
    # 일반적으로는 컴포넌트 초기화 시 initial_drawing 인자로 전달하지만,
    # 파일 업로드 후 동적으로 변경하는 것은 추가적인 로직이나 컴포넌트 지원이 필요합니다.
    # 임시 방편으로, 불러온 데이터를 확인하고 사용자에게 다시 그리도록 안내하거나,
    # 컴포넌트 업데이트를 통해 이 기능을 구현해야 합니다.
    st.sidebar.warning("불러온 JSON 데이터를 캔버스에 자동으로 적용하는 기능은 현재 제한적입니다. 파일을 확인해주세요.")
    st.sidebar.json(loaded_json_data) # 불러온 데이터 확인용

# 그린 내용을 이미지로 저장 (PNG)
if canvas_result.image_data is not None:
    st.sidebar.download_button(
        label="그린 내용 PNG로 저장",
        data=canvas_result.image_data,
        file_name="digital_whiteboard.png",
        mime="image/png"
    )

# --- 깔끔한 스타일 적용 (선택 사항) ---
# Streamlit은 기본적으로 깔끔한 스타일을 제공하지만, 추가적인 CSS를 적용할 수 있습니다.
st.markdown("""
<style>
    /* 전체 페이지 여백 줄이기 */
    .css-18e3th9, .css-1d3z3ef {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    /* 사이드바 너비 조절 */
    .css-1lcbmhc, .css-1ajxrlb {
        width: 300px;
    }
    /* 버튼 스타일 */
    div.stButton > button {
        width: 100%;
        border-radius: 5px;
    }
    /* 숫자 입력 필드 너비 조절 */
    .stNumberInput {
        width: 100%;
    }
    /* 타이머 표시 중앙 정렬 */
    h1 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 텍스트 추가 기능 설명 ---
st.markdown("""
**텍스트 추가 방법:**
1. 왼쪽 사이드바의 '그리기 모드'를 'text'로 선택합니다.
2. 캔버스에서 텍스트를 추가하고 싶은 위치를 클릭합니다.
3. 텍버스에 나타난 텍스트 상자에 원하는 내용을 입력합니다.
4. 텍스트 상자 바깥을 클릭하면 입력이 완료됩니다.
5. 'transform' 모드를 사용하여 텍스트의 위치나 크기를 조절할 수 있습니다.
""")
