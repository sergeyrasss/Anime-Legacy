import os
import subprocess
import math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def get_video_info(input_file):
    """Более надежное получение информации о видео"""
    try:
        # Получаем длительность (более надежный метод)
        cmd_duration = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '{input_file}'"
        duration = float(subprocess.check_output(cmd_duration, shell=True, text=True).strip())
        
        # Получаем разрешение
        cmd_res = f"ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 '{input_file}'"
        res = subprocess.check_output(cmd_res, shell=True, text=True).strip().split(',')
        width, height = int(res[0]), int(res[1])
        
        return duration, width, height
    except Exception as e:
        print(f"Ошибка анализа файла {input_file}: {str(e)}")
        raise

def calculate_bitrate(target_mb, duration_sec):
    """Расчет битрейта с проверкой"""
    if duration_sec <= 0:
        raise ValueError("Некорректная длительность видео")
    return int((target_mb * 8192) / duration_sec)

def convert_file(mkv_file, max_size_mb=90):
    """Улучшенная функция конвертации с обработкой ошибок"""
    mp4_file = mkv_file.with_suffix(".mp4")
    print(f"⚡ Обработка: {mkv_file.name}")
    
    try:
        # 1. Получаем параметры видео
        duration, width, height = get_video_info(mkv_file)
        
        # 2. Рассчитываем битрейт
        target_bitrate = calculate_bitrate(max_size_mb * 0.85, duration)
        
        # 3. Команда для конвертации с обработкой спецсимволов в имени
        safe_input = str(mkv_file).replace("'", "'\\''")
        safe_output = str(mp4_file).replace("'", "'\\''")
        
        cmd = (
            f"ffmpeg -i '{safe_input}' -threads 4 "
            "-c:v libx264 -preset fast -crf 23 "
            f"-b:v {target_bitrate}k -maxrate {target_bitrate}k "
            f"-bufsize {target_bitrate//2}k -vf scale={width//2*2}:{height//2*2} "
            "-c:a aac -b:a 96k -movflags +faststart -y "
            f"'{safe_output}'"
        )
        
        # 4. Запускаем конвертацию
        subprocess.run(cmd, shell=True, check=True)
        
        # 5. Проверяем результат
        if not mp4_file.exists():
            raise Exception("Файл не был создан")
            
        # 6. Удаляем исходник
        mkv_file.unlink()
        print(f"✅ Успешно: {mp4_file.name} ({os.path.getsize(mp4_file)//1048576} MB)")
        
    except Exception as e:
        print(f"❌ Ошибка при обработке {mk4_file.name}: {str(e)}")
        if mp4_file.exists():
            mp4_file.unlink()

def main():
    print("🚀 Улучшенный MKV в MP4 конвертер (max 90MB)")
    print("Используются многопоточность и надежные методы\n")
    
    mkv_files = list(Path.cwd().glob("*.mkv"))
    if not mkv_files:
        print("Не найдено MKV файлов в текущей директории.")
        return
    
    # Обработка файлов с ограничением потоков
    with ThreadPoolExecutor(max_workers=2) as executor:
        for file in mkv_files:
            executor.submit(convert_file, file)
    
    print("\nГотово! Результаты:")
    for mp4 in Path.cwd().glob("*.mp4"):
        size = os.path.getsize(mp4) // 1048576  # Размер в MB
        print(f"- {mp4.name} ({size} MB)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {str(e)}")
    input("\nНажмите Enter для выхода...")
