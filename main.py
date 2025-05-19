<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>수업용 디지털 도구</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f4f7f6; /* 부드러운 배경색 */
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #fff;
            border-radius: 12px; /* 둥근 모서리 */
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
            overflow: hidden;
        }
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #0056b3; /* 강조 색상 */
        }
        canvas {
            border: 1px solid #ddd;
            background-color: #fff;
            cursor: crosshair;
            touch-action: none; /* 터치 스크롤 방지 */
            display: block; /* 하단 여백 제거 */
            width: 100%; /* 부모 요소에 맞게 너비 조정 */
            height: auto; /* 높이 자동 조정 */
        }
        .button {
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            display: inline-flex; /* 아이콘과 텍스트 정렬 */
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }
        .button i {
            margin-right: 8px;
        }
        .button:hover {
            opacity: 0.9;
        }
        .button-primary {
            background-color: #007bff; /* 파란색 계열 */
            color: white;
            border: none;
        }
        .button-secondary {
            background-color: #6c757d; /* 회색 계열 */
            color: white;
            border: none;
        }
        .button-danger {
            background-color: #dc3545; /* 빨간색 계열 */
            color: white;
            border: none;
        }
        .input-field {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin-right: 10px;
            font-size: 1rem;
        }
        .timer-display {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            color: #28a745; /* 녹색 계열 */
        }
        .notification {
            text-align: center;
            color: #dc3545;
            font-weight: bold;
            margin-top: 15px;
            font-size: 1.2rem;
        }
        /* 반응형 디자인 */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            .section-title {
                font-size: 1.3rem;
            }
            .button {
                padding: 8px 12px;
                font-size: 0.9rem;
            }
            .input-field {
                padding: 8px;
                font-size: 0.9rem;
            }
            .timer-display {
                font-size: 2.5rem;
            }
        }
    </style>
</head>
<body class="bg-gray-100 p-4">
    <div class="container">
        <div class="p-6">
            <h1 class="text-2xl font-bold text-center mb-6 text-blue-700">수업용 디지털 도구</h1>

            <div class="mb-8">
                <h2 class="section-title">디지털 칠판</h2>
                <canvas id="whiteboard" class="w-full border border-gray-300 rounded-md shadow-sm"></canvas>
                <div class="flex flex-wrap gap-3 mt-4">
                    <button id="clearBtn" class="button button-danger"><i class="fas fa-eraser"></i> 모두 지우기</button>
                    <input type="text" id="textInput" class="input-field flex-grow" placeholder="캔버스에 추가할 텍스트 입력">
                    <button id="addTextBtn" class="button button-primary"><i class="fas fa-font"></i> 텍스트 추가</button>
                    <button id="saveBtn" class="button button-secondary"><i class="fas fa-save"></i> 저장</button>
                    <button id="loadBtn" class="button button-secondary"><i class="fas fa-folder-open"></i> 불러오기</button>
                </div>
            </div>

            <div>
                <h2 class="section-title">타이머</h2>
                <div class="flex flex-wrap items-center gap-3 mb-4">
                    <label for="minutes" class="font-semibold">분:</label>
                    <input type="number" id="minutes" class="input-field w-20" value="0" min="0">
                    <label for="seconds" class="font-semibold">초:</label>
                    <input type="number" id="seconds" class="input-field w-20" value="0" min="0" max="59">
                    <button id="setTimerBtn" class="button button-primary"><i class="fas fa-clock"></i> 시간 설정</button>
                </div>
                <div id="timerDisplay" class="timer-display">00:00</div>
                <div class="flex flex-wrap gap-3 justify-center">
                    <button id="startTimerBtn" class="button button-primary"><i class="fas fa-play"></i> 시작</button>
                    <button id="pauseTimerBtn" class="button button-secondary"><i class="fas fa-pause"></i> 일시정지</button>
                    <button id="resetTimerBtn" class="button button-danger"><i class="fas fa-sync-alt"></i> 재설정</button>
                </div>
                <div id="timerNotification" class="notification hidden">시간 종료!</div>
            </div>
        </div>
    </div>

    <script>
        // Canvas (디지털 칠판) 기능
        const canvas = document.getElementById('whiteboard');
        const ctx = canvas.getContext('2d');
        const clearBtn = document.getElementById('clearBtn');
        const textInput = document.getElementById('textInput');
        const addTextBtn = document.getElementById('addTextBtn');
        const saveBtn = document.getElementById('saveBtn');
        const loadBtn = document.getElementById('loadBtn');

        let drawing = false;
        let currentText = '';

        // 캔버스 크기 설정 (반응형)
        function resizeCanvas() {
            const container = canvas.parentElement;
            canvas.width = container.clientWidth;
            // 높이는 필요에 따라 고정하거나 비율로 설정할 수 있습니다.
            // 여기서는 너비에 비례하여 높이를 설정합니다.
            canvas.height = container.clientWidth * 0.6; // 예: 16:10 비율
            if (localStorage.getItem('canvasImage')) {
                 loadImageFromStorage(); // 크기 변경 시 저장된 이미지 다시 로드
            }
        }

        window.addEventListener('resize', resizeCanvas);
        resizeCanvas(); // 초기 로드 시 캔버스 크기 설정

        // 그리기 시작
        function startDrawing(e) {
            drawing = true;
            draw(e); // 시작점에서 점을 찍기 위해
        }

        // 그리기 중
        function draw(e) {
            if (!drawing) return;

            // 마우스 또는 터치 이벤트의 현재 위치 가져오기
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);

            if (clientX === undefined || clientY === undefined) return;

            // 캔버스 기준 좌표 계산
            const rect = canvas.getBoundingClientRect();
            const x = clientX - rect.left;
            const y = clientY - rect.top;

            ctx.lineWidth = 5; // 선 굵기
            ctx.lineCap = 'round'; // 선 끝 모양
            ctx.strokeStyle = '#000'; // 선 색상

            ctx.lineTo(x, y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(x, y);
        }

        // 그리기 종료
        function stopDrawing() {
            drawing = false;
            ctx.beginPath(); // 새로운 경로 시작
        }

        // 이벤트 리스너 등록 (마우스 및 터치)
        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mousemove', draw);

        canvas.addEventListener('touchstart', startDrawing);
        canvas.addEventListener('touchend', stopDrawing);
        canvas.addEventListener('touchmove', draw);

        // 모두 지우기 기능
        clearBtn.addEventListener('click', () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        });

        // 텍스트 추가 기능
        addTextBtn.addEventListener('click', () => {
            currentText = textInput.value;
            if (currentText.trim() !== '') {
                // 텍스트를 추가할 위치를 클릭으로 지정하도록 안내
                alert('캔버스에 텍스트를 추가할 위치를 클릭하세요.');
                canvas.addEventListener('click', addTextToCanvas, { once: true }); // 한 번만 실행
            } else {
                alert('추가할 텍스트를 입력하세요.');
            }
        });

        function addTextToCanvas(e) {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            ctx.font = '24px Inter'; // 폰트 설정
            ctx.fillStyle = '#000'; // 텍스트 색상
            ctx.fillText(currentText, x, y); // 텍스트 그리기

            textInput.value = ''; // 입력 필드 초기화
            currentText = ''; // 현재 텍스트 초기화
        }

        // 저장 기능 (localStorage 사용)
        saveBtn.addEventListener('click', () => {
            const dataURL = canvas.toDataURL(); // 캔버스 내용을 Data URL로 변환
            localStorage.setItem('canvasImage', dataURL);
            alert('캔버스 내용이 저장되었습니다.');
        });

        // 불러오기 기능 (localStorage 사용)
        loadBtn.addEventListener('click', () => {
            loadImageFromStorage();
        });

        function loadImageFromStorage() {
             const dataURL = localStorage.getItem('canvasImage');
             if (dataURL) {
                 const img = new Image();
                 img.onload = () => {
                     // 캔버스를 지우고 저장된 이미지를 그립니다.
                     ctx.clearRect(0, 0, canvas.width, canvas.height);
                     ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                 };
                 img.src = dataURL;
             } else {
                 alert('저장된 캔버스 내용이 없습니다.');
             }
        }


        // Timer (타이머) 기능
        const minutesInput = document.getElementById('minutes');
        const secondsInput = document.getElementById('seconds');
        const setTimerBtn = document.getElementById('setTimerBtn');
        const timerDisplay = document.getElementById('timerDisplay');
        const startTimerBtn = document.getElementById('startTimerBtn');
        const pauseTimerBtn = document.getElementById('pauseTimerBtn');
        const resetTimerBtn = document.getElementById('resetTimerBtn');
        const timerNotification = document.getElementById('timerNotification');

        let timerInterval = null;
        let totalSeconds = 0;
        let timeRemaining = 0;
        let isPaused = false;

        // 시간 설정
        setTimerBtn.addEventListener('click', () => {
            const minutes = parseInt(minutesInput.value) || 0;
            const seconds = parseInt(secondsInput.value) || 0;

            if (seconds < 0 || seconds > 59) {
                alert('초는 0에서 59 사이로 입력해주세요.');
                secondsInput.value = 0;
                return;
            }

            totalSeconds = (minutes * 60) + seconds;
            timeRemaining = totalSeconds;
            updateTimerDisplay();
            isPaused = false; // 시간 재설정 시 일시정지 상태 해제
            clearInterval(timerInterval); // 기존 타이머 중지
            timerNotification.classList.add('hidden'); // 알림 숨기기
        });

        // 타이머 시작
        startTimerBtn.addEventListener('click', () => {
            if (timeRemaining <= 0 && totalSeconds > 0) {
                // 시간이 다 되었지만, 다시 시작 버튼을 누른 경우 (재설정 없이)
                timeRemaining = totalSeconds;
                isPaused = false;
                timerNotification.classList.add('hidden');
            } else if (timeRemaining <= 0 && totalSeconds === 0) {
                 // 시간을 설정하지 않고 시작 버튼을 누른 경우
                 alert('타이머 시간을 먼저 설정해주세요.');
                 return;
            }

            if (timerInterval === null && !isPaused) { // 타이머가 실행 중이 아니고 일시정지 상태도 아닐 때
                 timerInterval = setInterval(updateTimer, 1000);
            } else if (isPaused) { // 일시정지 상태일 때 다시 시작
                 isPaused = false;
                 timerInterval = setInterval(updateTimer, 1000);
            }
             // 시작 버튼 비활성화 (선택 사항)
             // startTimerBtn.disabled = true;
        });

        // 타이머 일시정지
        pauseTimerBtn.addEventListener('click', () => {
            clearInterval(timerInterval);
            timerInterval = null;
            isPaused = true;
             // 시작 버튼 활성화 (선택 사항)
             // startTimerBtn.disabled = false;
        });

        // 타이머 재설정
        resetTimerBtn.addEventListener('click', () => {
            clearInterval(timerInterval);
            timerInterval = null;
            timeRemaining = totalSeconds; // 설정된 시간으로 재설정
            updateTimerDisplay();
            isPaused = false;
            timerNotification.classList.add('hidden'); // 알림 숨기기
             // 시작 버튼 활성화 (선택 사항)
             // startTimerBtn.disabled = false;
        });

        // 타이머 업데이트
        function updateTimer() {
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                timerInterval = null;
                timerNotification.classList.remove('hidden'); // 알림 표시
                // 시간이 다 되었을 때 추가 동작 (예: 소리 알림)을 여기에 추가할 수 있습니다.
                return;
            }

            timeRemaining--;
            updateTimerDisplay();
        }

        // 타이머 화면 표시 업데이트
        function updateTimerDisplay() {
            const minutes = Math.floor(timeRemaining / 60);
            const seconds = timeRemaining % 60;
            const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            timerDisplay.textContent = formattedTime;
        }

        // 초기 타이머 화면 표시
        updateTimerDisplay();

    </script>
</body>
</html>
