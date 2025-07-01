<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Плеер 5x для iOS 6</title>
    <style>
        body {
            font-family: Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 10px;
            background: #f0f0f0;
            -webkit-text-size-adjust: 100%;
        }
        .player-container {
            position: relative;
            margin: 10px 0;
            background: #000;
            border-radius: 3px;
            overflow: hidden;
        }
        #videoContainer {
            position: relative;
            width: 100%;
            height: 0;
            padding-bottom: 56.25%; /* 16:9 */
        }
        #videoPlayer, #hiddenPlayer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        #hiddenPlayer {
            opacity: 0;
            z-index: -1;
        }
        .controls {
            margin: 15px 0;
            padding: 10px;
            background: #fff;
            border-radius: 3px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }
        .speed-control {
            display: table;
            width: 100%;
            margin: 10px 0;
        }
        .speed-btn {
            display: table-cell;
            width: 40px;
            height: 40px;
            background: #4a6baf;
            color: white;
            text-align: center;
            vertical-align: middle;
            font-size: 20px;
            font-weight: bold;
            border-radius: 3px;
        }
        .speed-display {
            display: table-cell;
            text-align: center;
            vertical-align: middle;
            font-weight: bold;
            font-size: 16px;
        }
        input[type="range"] {
            width: 100%;
            margin: 15px 0;
            -webkit-appearance: none;
            height: 8px;
            background: #ddd;
            border-radius: 4px;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 20px;
            height: 20px;
            background: #4a6baf;
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <h1>Ускоренный плеер (до 5x)</h1>
    
    <div class="player-container">
        <div id="videoContainer">
            <!-- Видимый видеоплеер (только изображение) -->
            <video id="videoPlayer" webkit-playsinline playsinline></video>
            
            <!-- Скрытый плеер для аудио с максимальной скоростью -->
            <video id="hiddenPlayer" webkit-playsinline></video>
        </div>
    </div>
    
    <div class="controls">
        <div class="speed-control">
            <div id="decreaseSpeed" class="speed-btn">-</div>
            <div class="speed-display"><span id="currentSpeed">1.0x</span></div>
            <div id="increaseSpeed" class="speed-btn">+</div>
        </div>
        <input type="range" id="speedRange" min="0.5" max="5" step="0.1" value="1">
    </div>

    <script>
        // Конфигурация
        var videoUrl = 'video.mp4';
        var maxIOS6Speed = 2.0; // Максимальная скорость для iOS 6
        var targetSpeed = 1.0;
        var isIOS6 = /iP(hone|od|ad).*OS 6_/.test(navigator.userAgent);
        
        // Элементы
        var videoPlayer = document.getElementById('videoPlayer');
        var hiddenPlayer = document.getElementById('hiddenPlayer');
        var currentSpeed = document.getElementById('currentSpeed');
        var speedRange = document.getElementById('speedRange');
        
        // Инициализация плееров
        function initPlayers() {
            // Основной плеер (только видео)
            videoPlayer.src = videoUrl;
            videoPlayer.controls = false;
            videoPlayer.loop = true;
            
            // Скрытый плеер (аудио + максимальная скорость)
            hiddenPlayer.src = videoUrl;
            hiddenPlayer.volume = 1.0;
            
            // Синхронизация состояния
            videoPlayer.addEventListener('play', function() {
                hiddenPlayer.play().catch(e => console.log(e));
            });
            
            videoPlayer.addEventListener('pause', function() {
                hiddenPlayer.pause();
            });
            
            videoPlayer.addEventListener('seeked', function() {
                hiddenPlayer.currentTime = videoPlayer.currentTime;
            });
        }
        
        // Установка скорости
        function setPlaybackRate(rate) {
            targetSpeed = parseFloat(rate);
            updateSpeedDisplay();
            
            if(isIOS6) {
                // Для iOS 6 используем комбинацию скрытого плеера и визуального ускорения
                var visualRate = Math.min(maxIOS6Speed, targetSpeed);
                var audioRate = targetSpeed / visualRate;
                
                videoPlayer.playbackRate = visualRate;
                hiddenPlayer.playbackRate = audioRate;
                
                // Ускорение визуального воспроизведения через интервалы
                if(targetSpeed > maxIOS6Speed) {
                    startFrameAcceleration(visualRate);
                } else {
                    stopFrameAcceleration();
                }
            } else {
                videoPlayer.playbackRate = targetSpeed;
                hiddenPlayer.playbackRate = 1;
            }
        }
        
        // Переменные для ускорения кадров
        var accelerationInterval;
        var lastUpdate = 0;
        var frameStep = 0;
        
        function startFrameAcceleration(visualRate) {
            stopFrameAcceleration();
            var frameTime = 1000 / 30; // 30 fps
            
            accelerationInterval = setInterval(function() {
                var now = Date.now();
                if(now - lastUpdate >= frameTime) {
                    frameStep = (frameStep + 1) % 4;
                    if(frameStep === 0) {
                        videoPlayer.currentTime += 0.1 * visualRate;
                    }
                    lastUpdate = now;
                }
            }, frameTime / 4);
        }
        
        function stopFrameAcceleration() {
            if(accelerationInterval) {
                clearInterval(accelerationInterval);
                accelerationInterval = null;
            }
        }
        
        function updateSpeedDisplay() {
            currentSpeed.innerHTML = targetSpeed.toFixed(1) + 'x';
            speedRange.value = targetSpeed;
        }
        
        // Обработчики событий
        speedRange.addEventListener('input', function() {
            setPlaybackRate(this.value);
        });
        
        document.getElementById('increaseSpeed').addEventListener('click', function() {
            setPlaybackRate(targetSpeed + 0.1);
        });
        
        document.getElementById('decreaseSpeed').addEventListener('click', function() {
            setPlaybackRate(Math.max(0.5, targetSpeed - 0.1));
        });
        
        // Запуск при загрузке
        initPlayers();
        
        // Автовоспроизведение при касании (для iOS)
        document.body.addEventListener('touchend', function initPlay() {
            videoPlayer.play().catch(e => console.log(e));
            document.body.removeEventListener('touchend', initPlay);
        }, {once: true});
    </script>
</body>
</html>
