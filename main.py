import streamlit as st
import streamlit.components.v1 as components

# Streamlit 앱 설정
st.set_page_config(layout="wide") # 레이아웃을 넓게 설정
st.title("✨ Streamlit 디지털 칠판")
st.write("아래 영역에서 자유롭게 그림을 그리거나 내용을 작성하세요.")

# HTML, CSS, JavaScript 코드를 파이썬 문자열로 정의
# 그림 저장 및 불러오기 버튼 제거, 캔버스 높이 조정 로직 수정
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>디지털 칠판 컴포넌트</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* 기본 스타일 및 초기화 */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            background-color: #fff; /* Streamlit 배경색과 맞추거나 투명하게 */
            color: #333;
            /* Streamlit에 임베드될 때는 body 패딩이나 마진을 제거하는 것이 좋습니다. */
            padding: 0;
            margin: 0;
            overflow: hidden; /* 스크롤 방지 */
            width: 100%;
            height: 100%; /* Ensure body takes full height of the component iframe */
            display: flex; /* Use flexbox for body to manage container height */
            flex-direction: column;
        }

        #whiteboard-container {
            width: 100%;
            flex-grow: 1; /* Allow container to grow and fill body height */
            display: flex;
            flex-direction: column;
            background-color: #fff; /* 칠판 배경색 */
            border-radius: 8px; /* Streamlit 컨테이너와 일관성 유지 */
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 그림자 */
            overflow: hidden; /* 내용 넘침 방지 */
        }

        #whiteboard-controls {
            padding: 10px;
            background-color: #f0f2f6; /* Streamlit 사이드바/컨트롤 색상과 유사하게 */
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
            justify-content: center; /* 버튼 중앙 정렬 */
            border-bottom: 1px solid #eee;
            flex-shrink: 0; /* Prevent controls from shrinking */
        }

        #whiteboard-controls button {
             padding: 8px 15px;
             border: none;
             border-radius: 4px;
             cursor: pointer;
             font-size: 0.9rem; /* 글씨 크기 약간 줄임 */
             display: flex;
             align-items: center;
             gap: 5px;
             transition: background-color 0.2s ease;
             font-weight: bold;
        }

        #clearBtn {
            background-color: #ff4d4d;
            color: white;
        }
        #clearBtn:hover { background-color: #ff1a1a; }

        /* 저장/불러오기 버튼 관련 스타일은 제거 */

        #drawingCanvas {
            flex-grow: 1; /* Allow canvas to grow and fill remaining space */
            flex-shrink: 1; /* Allow canvas to shrink */
            flex-basis: auto; /* Default basis */
            background-color: #fff; /* 칠판 배경색 */
            cursor: crosshair;
            /* 캔버스 자체의 너비/높이는 JavaScript로 설정 */
            display: block; /* Ensure canvas is a block element */
        }

        /* 모바일 반응형 조정 */
        @media (max-width: 768px) {
            #whiteboard-controls {
                 flex-direction: column; /* 모바일에서 버튼 세로 정렬 */
                 align-items: stretch; /* 버튼 너비 맞춤 */
            }
             #whiteboard-controls button {
                 justify-content: center; /* 모바일 버튼 내용 중앙 정렬 */
             }
        }
    </style>
</head>
<body>

    <div id="whiteboard-container">
        <div id="whiteboard-controls">
            <button id="clearBtn"><i class="fas fa-eraser"></i> 모두 지우기</button>
        </div>
        <canvas id="drawingCanvas"></canvas>
    </div>


    <script>
        // JavaScript 코드 시작

        // --- 디지털 칠판 기능 ---
        const canvas = document.getElementById('drawingCanvas');
        const ctx = canvas.getContext('2d');
        const clearBtn = document.getElementById('clearBtn');
        const container = document.getElementById('whiteboard-container');
        const controls = document.getElementById('whiteboard-controls');


        let drawing = false;
        let lastX = 0;
        let lastY = 0;

        // 캔버스 크기 조정 (반응형)
        const resizeCanvas = () => {
             // Set the canvas's internal drawing buffer size to match its *actual* display size
             // as determined by CSS Flexbox. This prevents drawing distortion.
             canvas.width = canvas.offsetWidth;
             canvas.height = canvas.offsetHeight;

             // Note: resizing canvas clears its content.
             // Since save/load is removed, no need to attempt re-drawing.
        };

        // 초기 로드 시 및 윈도우 크기 변경 시 캔버스 크기 조정
        // 윈도우 로드 시 캔버스 크기 초기 설정
        window.onload = () => {
            resizeCanvas();
        };
        window.addEventListener('resize', resizeCanvas);


        // 드로잉 시작 (마우스 및 터치)
        function startDrawing(e) {
            drawing = true;
            // 캔버스 기준 좌표 계산
            const rect = canvas.getBoundingClientRect();
            let clientX, clientY;

            if (e.type.includes('mouse')) {
                clientX = e.offsetX;
                clientY = e.offsetY;
            } else if (e.type.includes('touch')) {
                 // 터치 좌표 계산
                clientX = e.touches[0].clientX - rect.left;
                clientY = e.touches[0].clientY - rect.top;
                e.preventDefault(); // 터치 스크롤 방지
            } else {
                 return; // 지원하지 않는 이벤트 타입
            }

            // Adjust coordinates for potential CSS scaling if needed (though Flexbox should handle this)
            // const scaleX = canvas.width / rect.width;
            // const scaleY = canvas.height / rect.height;
            // [lastX, lastY] = [(clientX - rect.left) * scaleX, (clientY - rect.top) * scaleY];
             [lastX, lastY] = [clientX, clientY];
        }

        // 드로잉 중 (마우스 및 터치)
        function draw(e) {
            if (!drawing) return;
            const rect = canvas.getBoundingClientRect();
            let clientX, clientY;

            if (e.type.includes('mouse')) {
                clientX = e.offsetX;
                clientY = e.offsetY;
            } else if (e.type.includes('touch')) {
                 // 터치 좌표 계산
                clientX = e.touches[0].clientX - rect.left;
                clientY = e.touches[0].clientY - rect.top;
                e.preventDefault(); // 터치 스크롤 방지
            } else {
                 return; // 지원하지 않는 이벤트 타입
            }

            // Adjust coordinates for potential CSS scaling if needed
            // const scaleX = canvas.width / rect.width;
            // const scaleY = canvas.height / rect.height;
            // const currentX = (clientX - rect.left) * scaleX;
            // const currentY = (clientY - rect.top) * scaleY;
             const currentX = clientX;
             const currentY = clientY;


            ctx.strokeStyle = '#000'; // 검은색
            ctx.lineJoin = 'round';
            ctx.lineCap = 'round';
            ctx.lineWidth = 5; // 선 굵기

            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineTo(currentX, currentY);
            ctx.stroke();
            [lastX, lastY] = [currentX, currentY];
        }

        // 드로잉 중지 (마우스 및 터치)
        function stopDrawing() {
            drawing = false;
        }

        // 이벤트 리스너 연결 (마우스 및 터치)
        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseout', stopDrawing); // 캔버스 밖으로 나갔을 때 중지

        canvas.addEventListener('touchstart', startDrawing);
        canvas.addEventListener('touchmove', draw);
        canvas.addEventListener('touchend', stopDrawing);
        canvas.addEventListener('touchcancel', stopDrawing);

        // 모두 지우기 기능
        clearBtn.addEventListener('click', () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        });

        // 저장/불러오기 기능 관련 JavaScript 코드 제거

        // JavaScript 코드 끝
    </script>

</body>
</html>
"""

# Streamlit 컴포넌트로 HTML 코드 렌더링
# height 값을 더 크게 조정하여 세로 화면을 거의 채우도록 설정
# 적절한 높이 값은 사용자의 화면 해상도에 따라 다를 수 있으나,
# 여기서는 1500 픽셀로 설정하여 대부분의 화면에서 크게 보이도록 합니다.
components.html(html_code, height=1500, scrolling=False) # height 값을 1500으로 유지 또는 더 크게 조정 가능

st.markdown("---")
st.write("**참고:** 그림 저장 및 불러오기 기능은 제거되었습니다. '모두 지우기' 기능만 사용 가능합니다.")
