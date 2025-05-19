import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import time

st.set_page_config(page_title="디지털 칠판", layout="wide")

st.title("📚 디지털 칠판")

# Session state 초기화
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = 0

### 좌측: 디지털 칠판 ###
with st.sidebar:
    st.header("🖍️ 칠판 도구")
    
    drawing_mode = st.selectbox("그리기 도구", ("freedraw", "line", "rect", "circle", "transform"))
    stroke_width = st.slider("선 굵기", 1, 25, 3)
    stroke_color = st.color_picker("선 색상", "#000000")
    bg_color = st.color_picker("배경 색상", "#FFFFFF")
    
    add_text = st.text_input("추가할 텍스트")
    if st.button("텍스트 위치 선택 후 추가"):
        st.session_state.add_text_mode = True

    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)", 
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=500,
        drawing_mode=drawing_mode,
        key="canvas",
    )

    if st.button("🧹 모두 지우기"):
        st.experimental_rerun()

    # 저장
    if st.button("💾 이미지 저장"):
        if canvas_result.image_data is not None:
            img = Image.fromarray(canvas_result.image_data.astype('uint8'))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("이미지 다운로드", buf.getvalue(), file_name="chalkboard.png", mime="image/png")

    # 불러오기
    uploaded_file = st.file_uploader("이미지 불러오기", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="불러온 이미지")

### 우측: 타이머 ###
with st.container():
    st.header("⏲️ 타이머")

    col1, col2 = st.columns(2)
    with col1:
        minutes = st.number_input("분", min_value=0, max_value=120, step=1)
    with col2:
        seconds = st.number_input("초", min_value=0, max_value=59, step=1)

    def format_time(t):
        mins, secs = divmod(int(t), 60)
        return f"{mins:02d}:{secs:02d}"

    if st.button("시작"):
        st.session_state.start_time = time.time()
        st.session_state.remaining_time = minutes * 60 + seconds
        st.session_state.timer_running = True

    if st.button("일시정지"):
        st.session_state.timer_running = False

    if st.button("재설정"):
        st.session_state.timer_running = False
        st.session_state.remaining_time = minutes * 60 + seconds

    if st.session_state.timer_running:
        elapsed = time.time() - st.session_state.start_time
        st.session_state.remaining_time -= elapsed
        st.session_state.start_time = time.time()

        if st.session_state.remaining_time <= 0:
            st.session_state.timer_running = False
            st.success("⏰ 시간이 종료되었습니다!")
            st.markdown("<audio autoplay><source src='https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3' type='audio/mpeg'></audio>", unsafe_allow_html=True)

    st.subheader(f"남은 시간: {format_time(st.session_state.remaining_time)}")
