import streamlit as st
import time
import base64

# Function to add background image
def add_bg_from_local(image_file):
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

with col1:
    hours = st.number_input("시간", min_value=0, max_value=23, value=0, step=1)
with col2:
    minutes = st.number_input("분", min_value=0, max_value=59, value=0, step=1)
with col3:
    seconds = st.number_input("초", min_value=0, max_value=59, value=0, step=1)

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

start_button = st.button("타이머 시작")
stop_button = st.button("타이머 중지")
reset_button = st.button("타이머 초기화")

# 타이머 디스플레이를 위한 placeholder
timer_placeholder = st.empty()

if start_button and total_seconds > 0:
    st.session_state.timer_running = True
    st.session_state.total_duration = total_seconds
    st.session_state.start_time = time.time()
    st.session_state.end_time = st.session_state.start_time + total_seconds
elif start_button and total_seconds == 0:
    st.warning("시간을 설정해주세요!")

if stop_button:
    st.session_state.timer_running = False
    # 남은 시간을 계산하여 저장 (다시 시작 시 이어서)
    if st.session_state.start_time is not None:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, st.session_state.total_duration - elapsed)
        st.session_state.total_duration = remaining # 남은 시간을 새로운 총 시간으로 설정
    st.session_state.start_time = None # 시작 시간 초기화

if reset_button:
    st.session_state.timer_running = False
    st.session_state.start_time = None
    st.session_state.end_time = None
    st.session_state.total_duration = 0
    timer_placeholder.markdown("## ⏳ 00:00:00") # 초기화 시 디스플레이 초기화

# --- 타이머 카운트다운 로직 ---
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
        timer_placeholder.markdown("## 🎉 시간 종료! 🎉", unsafe_allow_html=True)
        st.balloons() # 풍선 효과 추가!

# 타이머가 시작되지 않았거나 중지된 상태일 때 마지막 남은 시간 표시
elif st.session_state.total_duration > 0 and st.session_state.start_time is None:
     remaining_time = st.session_state.total_duration
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
else:
    # 초기 상태 또는 리셋 상태일 때
    timer_placeholder.markdown("## ⏳ 00:00:00")

# --- 추가적인 화려함 (선택 사항) ---
st.markdown("---")
st.write("✨ 즐거운 시간 보내세요! ✨")

# 배경 이미지 사용 시, 'your_background_image.jpg' 파일을 이 스크립트와 같은 폴더에 넣어주세요.
# 또는 add_bg_from_local 함수 호출 부분을 주석 처리하거나 삭제하세요.
