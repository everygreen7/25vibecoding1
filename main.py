import streamlit as st
import streamlit.components.v1 as components

# Streamlit 앱 설정
st.set_page_config(layout="wide") # 레이아웃을 넓게 설정
st.title("✨ Streamlit 디지털 칠판")
st.write("아래 영역에서 자유롭게 그림을 그리거나 내용을 작성하세요.")

# HTML, CSS, JavaScript 코드를 파이썬 문자열로 정의
# 이 코드는 이전에 제공된 디지털 칠판 HTML 코드와 동일합니다.
# Streamlit 컴포넌트 내에서 실행되도록 약간의 조정이 필요할 수 있지만,
# 기본적인 HTML/CSS/JS는 그대로 사용할 수 있습니다.
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
            /* padding: 0; */
            /* margin: 0; */
            overflow: hidden; /* 스크롤 방지 */
        }

        #whiteboard-container {
            width: 100%;
            height: 100%; /* 부모(컴포넌트) 높이에 맞춤 */
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

        #saveDrawingBtn, #loadDrawingBtn {
             background-color: #007bff;
             color: white;
        }
        #saveDrawingBtn:hover, #loadDrawingBtn:hover { background-color: #0056b3; }

        #drawingCanvas {
            flex-grow: 1; /* 남은 공간 모두 사용 */
            background-color: #fff; /* 칠판 배경색 */
            cursor: crosshair;
            /* 캔버스 자체의 너비/높이는 JavaScript로 설정 */
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
            <button id="saveDrawingBtn"><i class="fas fa-save"></i> 그림 저장 (브라우저)</button>
            <button id="loadDrawingBtn"><i class="fas fa-upload"></i> 그림 불러오기 (브라우저)</button>
             </div>
        <canvas id="drawingCanvas"></canvas>
    </div>


    <script>
        // JavaScript 코드 시작

        // --- 디지털 칠판 기능 ---
        const canvas = document.getElementById('drawingCanvas');
        const ctx = canvas.getContext('2d');
        const clearBtn = document.getElementById('clearBtn');
        const saveDrawingBtn = document.getElementById('saveDrawingBtn');
        const loadDrawingBtn = document.getElementById('loadDrawingBtn');
        const container = document.getElementById('whiteboard-container');


        let drawing = false;
        let lastX = 0;
        let lastY = 0;

        // 캔버스 크기 조정 (반응형)
        const resizeCanvas = () => {
             // 부모 컨테이너 크기에 맞게 캔버스 크기 조정
             canvas.width = container.offsetWidth;
             // 컨트롤 영역 높이를 뺀 나머지 공간을 캔버스 높이로 사용
             const controlsHeight = document.getElementById('whiteboard-controls').offsetHeight;
             canvas.height = container.offsetHeight - controlsHeight;


             // Note: resizing canvas clears its content. Need to re-draw if state exists.
             // For simplicity, we will attempt to reload the drawing after resize if one exists.
             const savedDrawing = localStorage.getItem('savedDrawing');
             if (savedDrawing) {
                 const img = new Image();
                 img.onload = () => {
                     // 기존 내용을 지우고 저장된 그림을 현재 크기에 맞게 다시 그립니다.
                     ctx.clearRect(0, 0, canvas.width, canvas.height);
                     // 저장된 이미지의 비율을 유지하면서 현재 캔버스에 맞게 그립니다.
                     const hRatio = canvas.width / img.width;
                     const vRatio = canvas.height / img.height;
                     const ratio = Math.min(hRatio, vRatio);
                     const centerShift_x = (canvas.width - img.width * ratio) / 2;
                     const centerShift_y = (canvas.height - img.height * ratio) / 2;
                     ctx.drawImage(img, 0, 0, img.width, img.height,
                                   centerShift_x, centerShift_y, img.width * ratio, img.height * ratio);
                 };
                 img.src = savedDrawing;
             }
        };

        // 초기 로드 시 및 윈도우 크기 변경 시 캔버스 크기 조정
        // 윈도우 로드 시 캔버스 크기 조정 및 저장된 그림 불러오기 시도
        window.onload = () => {
            resizeCanvas(); // 캔버스 크기 초기 설정 및 저장된 그림 불러오기 시도
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


            ctx.strokeStyle = '#000'; // 검은색
            ctx.lineJoin = 'round';
            ctx.lineCap = 'round';
            ctx.lineWidth = 5; // 선 굵기

            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineTo(clientX, clientY);
            ctx.stroke();
            [lastX, lastY] = [clientX, clientY];
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

        // 그림 저장 (localStorage)
        saveDrawingBtn.addEventListener('click', () => {
            try {
                const dataURL = canvas.toDataURL(); // 캔버스 내용을 Data URL 형식으로 가져옴
                localStorage.setItem('savedDrawing', dataURL);
                alert('그림이 브라우저에 저장되었습니다.');
            } catch (e) {
                alert('그림 저장 중 오류가 발생했습니다. 브라우저 저장 공간이 부족하거나 지원되지 않을 수 있습니다.');
                console.error(e);
            }
        });

        // 그림 불러오기 (localStorage)
        loadDrawingBtn.addEventListener('click', () => {
            const savedDrawing = localStorage.getItem('savedDrawing');
            if (savedDrawing) {
                const img = new Image();
                img.onload = () => {
                    // 캔버스 크기가 변경되었을 수 있으므로 불러온 이미지를 현재 캔버스 크기에 맞게 그립니다.
                    // 비율 유지는 필요에 따라 조절해야 합니다. 여기서는 간단히 캔버스 전체를 채우도록 합니다.
                    ctx.clearRect(0, 0, canvas.width, canvas.height); // 기존 내용 지우고
                     const hRatio = canvas.width / img.width;
                     const vRatio = canvas.height / img.height;
                     const ratio = Math.min(hRatio, vRatio);
                     const centerShift_x = (canvas.width - img.width * ratio) / 2;
                     const centerShift_y = (canvas.height - img.height * ratio) / 2;
                     ctx.drawImage(img, 0, 0, img.width, img.height,
                                   centerShift_x, centerShift_y, img.width * ratio, img.height * ratio);
                };
                img.src = savedDrawing;
                 alert('그림을 브라우저에서 불러왔습니다.');
            } else {
                alert('저장된 그림이 없습니다.');
            }
        });

        // JavaScript 코드 끝
    </script>

</body>
</html>
"""

# Streamlit 컴포넌트로 HTML 코드 렌더링
# height 값을 조정하여 칠판 영역의 높이를 설정할 수 있습니다.
# scrolling=True로 설정하면 칠판 영역이 넘칠 때 스크롤바가 생깁니다.
components.html(html_code, height=1000, scrolling=False) # height 값을 1000으로 증가

st.markdown("---")
st.write("**참고:** 그림 저장 및 불러오기 기능은 현재 브라우저의 로컬 저장소(localStorage)를 사용합니다. 다른 브라우저나 기기에서는 공유되지 않습니다.")

