import streamlit as st
import time
import base64

# Function to add background image
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f"배경 이미지 파일을 찾을 수 없습니다: {image_file}")
    except Exception as e:
        st.warning(f"배경 이미지 설정 중 오류 발생: {e}")


# --- 커스텀 CSS 추가: 입력 필드 크기 조절 ---
st.markdown("""
<style>
/* Streamlit 숫자 입력 필드의 입력 부분 (input 태그)을 타겟팅 */
div[data-testid="stNumberInput"] input {
    font-size: 1.5em !important; /* 글자 크기 키우기 */
    padding: 10px !important; /* 패딩 추가하여 필드 자체 크기 키우기 */
    height: auto !important; /* 높이 자동 조절 */
}

/* 숫자 입력 필드의 레이블 (label 태그) 크기 조절 */
div[data-testid="stNumberInput"] label {
    font-size: 1.2em !important; /* 레이블 글자 크기 키우기 */
    font-weight: bold !important;
}

/* 전체 앱의 글꼴 및 기본 스타일 */
html, body, [class*="st"] {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 타이머 디스플레이 중앙 정렬 및 스타일 */
div[data-testid="stEmpty"] > div {
    text-align: center;
    font-size: 4em;
    font-weight: bold;
    color: #FF4B4B; /* Streamlit primary color */
    text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# --- 웹 앱 타이틀 및 설명 ---
st.title("✨ 화려한 카운트다운 타이머 ✨")
st.markdown("""
설정된 시간부터 0까지 카운트다운하는 타이머입니다.
원하는 시간, 분, 초를 설정하고 '타이머 시작' 버튼을 눌러주세요!
""")

# --- 배경 이미지 설정 (로컬 이미지 파일 경로를 넣어주세요!) ---
# 예시: add_bg_from_local('background.jpg')
# 로컬 이미지가 없으면 이 줄을 주석 처리하거나 삭제하세요.
# add_bg_from_local('your_background_image.jpg') # <-- 여기에 이미지 파일 경로를 입력하세요!

# --- 타이머 설정 입력 ---
st.header("⏰ 시간 설정")

col1, col2, col3 = st.columns(3)

# 세션 상태에 입력 필드 초기값 설정 (리셋 시 사용)
if 'hours_input_value' not in st.session_state:
    st.session_state.hours_input_value = 0
if 'minutes_input_value' not in st.session_state:
    st.session_state.minutes_input_value = 0
if 'seconds_input_value' not in st.session_state:
    st.session_state.seconds_input_value = 0


with col1:
    # value를 세션 상태 변수로 연결
    hours = st.number_input("시간", min_value=0, max_value=23, step=1, key='hours_input', value=st.session_state.hours_input_value)
with col2:
    # value를 세션 상태 변수로 연결
    minutes = st.number_input("분", min_value=0, max_value=59, step=1, key='minutes_input', value=st.session_state.minutes_input_value)
with col3:
    # value를 세션 상태 변수로 연결
    seconds = st.number_input("초", min_value=0, max_value=59, step=1, key='seconds_input', value=st.session_state.seconds_input_value)

total_seconds = hours * 3600 + minutes * 60 + seconds

# --- 타이머 시작 버튼 및 로직 ---
st.header("▶️ 타이머 실행")

# 타이머 시작 상태를 세션 상태에 저장
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'total_duration' not in st.session_state:
     st.session_state.total_duration = 0
if 'last_remaining' not in st.session_state: # 중지 후 남은 시간 저장을 위한 변수
     st.session_state.last_remaining = 0


start_button = st.button("타이머 시작")
stop_button = st.button("타이머 중지")
reset_button = st.button("타이머 초기화")

# 타이머 디스플레이를 위한 placeholder
timer_placeholder = st.empty()

# 초기 또는 리셋 상태일 때 디스플레이
if not st.session_state.timer_running and st.session_state.last_remaining == 0:
     timer_placeholder.markdown("## ⏳ 00:00:00", unsafe_allow_html=True)
elif not st.session_state.timer_running and st.session_state.last_remaining > 0:
    # 중지 상태일 때 마지막 남은 시간 표시
    remaining_time = st.session_state.last_remaining
    hours_display = int(remaining_time // 3600)
    minutes_display = int((remaining_time % 3600) // 60)
    seconds_display = int(remaining_time % 60)
    timer_html = f"""
    <div style="
        text-align: center;
        font-size: 4em;
        font-weight: bold;
        color: #FF4B4B; /* Streamlit primary color */
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        margin-top: 20px;
    ">
        {hours_display:02d}:{minutes_display:02d}:{seconds_display:02d}
    </div>
    """
    timer_placeholder.markdown(timer_html, unsafe_allow_html=True)


if start_button:
    if total_seconds > 0 or st.session_state.last_remaining > 0:
        if not st.session_state.timer_running:
            # 중지 후 다시 시작하는 경우 남은 시간부터 시작
            if st.session_state.last_remaining > 0:
                st.session_state.total_duration = st.session_state.last_remaining
            # 새로 시작하는 경우
            else:
                 st.session_state.total_duration = total_seconds

            st.session_state.start_time = time.time()
            st.session_state.end_time = st.session_state.start_time + st.session_state.total_duration
            st.session_state.timer_running = True
            st.session_state.last_remaining = 0 # 다시 시작했으므로 남은 시간 초기화
            st.rerun() # 타이머 시작 후 바로 UI 업데이트를 위해 rerun

        else:
             st.warning("타이머가 이미 실행 중입니다.")
    else:
        st.warning("시간을 설정해주세요!")


if stop_button:
    if st.session_state.timer_running:
        st.session_state.timer_running = False
        # 남은 시간을 계산하여 저장 (다시 시작 시 이어서)
        if st.session_state.start_time is not None:
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, st.session_state.total_duration - elapsed)
            st.session_state.last_remaining = remaining # 남은 시간을 저장
        st.session_state.start_time = None # 시작 시간 초기화
        st.rerun() # 중지 후 UI 업데이트를 위해 rerun
    else:
        st.info("타이머가 실행 중이 아닙니다.")


if reset_button:
    st.session_state.timer_running = False
    st.session_state.start_time = None
    st.session_state.end_time = None
    st.session_state.total_duration = 0
    st.session_state.last_remaining = 0
    # 입력 필드 값 초기화를 위한 세션 상태 변수 설정
    st.session_state.hours_input_value = 0
    st.session_state.minutes_input_value = 0
    st.session_state.seconds_input_value = 0
    st.rerun() # 상태 변경 후 새로고침하여 입력 필드 값 반영


# --- 타이머 카운트다운 로직 ---
# 타이머가 실행 중일 때만 이 블록 실행
if st.session_state.timer_running and st.session_state.end_time is not None:
    while time.time() < st.session_state.end_time:
        remaining_time = st.session_state.end_time - time.time()
        if remaining_time < 0:
            remaining_time = 0 # Ensure it doesn't show negative time

        hours_display = int(remaining_time // 3600)
        minutes_display = int((remaining_time % 3600) // 60)
        seconds_display = int(remaining_time % 60)

        # 화려한 디스플레이를 위해 HTML/CSS 사용
        timer_html = f"""
        <div style="
            text-align: center;
            font-size: 4em;
            font-weight: bold;
            color: #FF4B4B; /* Streamlit primary color */
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            margin-top: 20px;
        ">
            {hours_display:02d}:{minutes_display:02d}:{seconds_display:02d}
        </div>
        """
        timer_placeholder.markdown(timer_html, unsafe_allow_html=True)
        time.sleep(0.1) # 0.1초마다 업데이트하여 부드럽게 보이게 함

    # 타이머 종료 시 메시지
    if st.session_state.timer_running: # 종료 시에도 timer_running이 True인 경우 (자연 종료)
        st.session_state.timer_running = False
        st.session_state.last_remaining = 0 # 종료되었으므로 남은 시간 없음
        timer_placeholder.markdown("## 🎉 시간 종료! 🎉", unsafe_allow_html=True)
        st.balloons() # 풍선 효과 추가!
        st.rerun() # 종료 후 상태 변경 반영


# --- 추가적인 화려함 (선택 사항) ---
st.markdown("---")
st.write("✨ 즐거운 시간 보내세요! ✨")

# 배경 이미지 사용 시, 'your_background_image.jpg' 파일을 이 스크립트와 같은 폴더에 넣어주세요.
# 또는 add_bg_from_local 함수 호출 부분을 주석 처리하거나 삭제하세요.
