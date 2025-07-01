<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Видеоплеер для iOS 6</title>
    <style>
        body {
            font-family: Helvetica, Arial, sans-serif;
            text-align: center;
            padding: 15px;
            background: #f0f0f0;
        }
        #playerContainer {
            margin: 20px auto;
            width: 100%;
            max-width: 640px;
        }
        #fallbackMessage {
            color: #cc0000;
            font-weight: bold;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Видеоплеер</h1>
    
    <div id="playerContainer">
        <!-- Стандартный HTML5 плеер -->
        <video id="html5Player" width="100%" controls webkit-playsinline>
            <source src="video.mp4" type="video/mp4">
            Ваш браузер не поддерживает HTML5 видео.
        </video>
        
        <!-- Fallback для iOS 6 -->
        <div id="fallbackMessage" style="display:none;">
            <p>Используется специальный режим для iOS 6</p>
            <iframe id="ios6Player" width="100%" height="360" frameborder="0" allowfullscreen></iframe>
        </div>
    </div>

    <script>
        // Определяем iOS 6
        var isIOS6 = /iP(hone|od|ad).*OS 6_/.test(navigator.userAgent);
        var videoUrl = 'video.mp4';
        
        if(isIOS6) {
            // Скрываем стандартный плеер
            document.getElementById('html5Player').style.display = 'none';
            
            // Показываем fallback-сообщение
            document.getElementById('fallbackMessage').style.display = 'block';
            
            // Создаем специальный плеер для iOS 6
            document.getElementById('ios6Player').src = videoUrl;
            
            // Альтернативный метод для кнопки воспроизведения
            document.body.addEventListener('click', function() {
                document.getElementById('ios6Player').src = videoUrl + '?autoplay=1';
            });
        }
    </script>
</body>
</html>
