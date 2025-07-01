<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Видео для iOS 6</title>
    <style>
        body { 
            font-family: Helvetica, sans-serif;
            text-align: center;
            padding: 20px;
            background: #f0f0f0;
        }
        .player-container {
            margin: 0 auto;
            width: 100%;
            max-width: 640px;
        }
        .download-btn {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background: #4a6baf;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Видео контент</h1>
    
    <div class="player-container">
        <!-- 1. Попытка встроенного воспроизведения -->
        <object width="100%" height="360"
            classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B"
            codebase="http://www.apple.com/qtactivex/qtplugin.cab">
            <param name="src" value="video.mp4">
            <param name="autoplay" value="false">
            <param name="controller" value="true">
            <embed src="video.mp4" width="100%" height="360"
                autoplay="false" controller="true"
                pluginspage="http://www.apple.com/quicktime/download/">
        </object>
        
        <!-- 2. Альтернатива для современных iOS -->
        <video width="100%" controls style="display:none;">
            <source src="video.mp4" type="video/mp4">
        </video>
        
        <!-- 3. Ссылка для скачивания -->
        <a href="video.mp4" class="download-btn">
            Скачать видео для просмотра
        </a>
    </div>

    <script>
        // Автоматическое переключение между технологиями
        if(navigator.userAgent.match(/iPhone|iPad|iPod/i)) {
            document.querySelector('object').style.display = 'none';
            document.querySelector('video').style.display = 'block';
        }
    </script>
</body>
</html>
