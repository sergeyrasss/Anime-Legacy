import os
import subprocess
import math
from pathlib import Path

def get_video_duration(input_file):
    """Получает длительность видео в секундах"""
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '{input_file}'"
    try:
        duration = float(subprocess.check_output(cmd, shell=True, text=True).strip())
        return duration
    except Exception as e:
        print(f"Ошибка при получении длительности: {str(e)}")
        return 0

def calculate_bitrate(target_mb, duration_sec, audio_bitrate=128):
    """Вычисляет требуемый видеобитрейт для целевого размера"""
    if duration_sec <= 0:
        return 1500  # Значение по умолчанию
    
    target_kb = target_mb * 1024
    audio_kb = (audio_bitrate * duration_sec) / 8
    available_kb = target_kb - audio_kb
    return int((available_kb * 8) / duration_sec)

def convert_to_ios6_compatible(input_file, output_file, max_size_mb=90):
    """Конвертирует видео в формат, совместимый с iOS 6 с гарантированным контролем размера"""
    try:
        # 1. Получаем длительность видео
        duration = get_video_duration(input_file)
        if duration <= 0:
            print("⚠️ Не удалось получить длительность видео, используется битрейт по умолчанию")
            video_bitrate = 1500
        else:
            # 2. Рассчитываем битрейт для 80% от целевого размера
            video_bitrate = calculate_bitrate(max_size_mb * 0.8, duration)
            video_bitrate = max(500, min(video_bitrate, 3000))  # Ограничиваем диапазон
            print(f"ℹ️ Используемый битрейт: {video_bitrate}k, Длительность: {duration:.1f} сек")
        
        # 3. Параметры конвертации
        cmd = (
            f"ffmpeg -i '{input_file}' "
            "-c:v libx264 -profile:v baseline -level 3.0 "
            f"-b:v {video_bitrate}k -maxrate {video_bitrate}k -bufsize {video_bitrate * 2}k "
            "-pix_fmt yuv420p -vf 'scale=640:trunc(ow/a/2)*2' "
            "-c:a aac -b:a 96k "  # Уменьшаем аудиобитрейт
            "-movflags +faststart "
            "-r 24 -g 48 "  # Фиксируем частоту кадров
            f"'{output_file}'"
        )
        
        # 4. Запуск конвертации
        print("🔄 Начало конвертации...")
        result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)
        
        # 5. Проверка ошибок
        if result.returncode != 0:
            print(f"❌ Ошибка конвертации: {result.stderr[:500]}...")  # Выводим только начало ошибки
            return False
        
        # 6. Проверка существования выходного файла
        if not Path(output_file).exists():
            print("❌ Выходной файл не создан")
            return False
        
        # 7. Проверка размера и пережатие при необходимости
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        if size_mb > max_size_mb:
            print(f"⚠️ Размер файла {size_mb:.2f} MB > {max_size_mb} MB, оптимизируем...")
            return recompress_file(output_file, max_size_mb)
        
        return True
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {str(e)}")
        return False

def recompress_file(input_file, max_size_mb):
    """Пережимает файл до нужного размера с более агрессивными настройками"""
    try:
        # 1. Получаем длительность
        duration = get_video_duration(input_file)
        if duration <= 0:
            print("❌ Не удалось получить длительность для пережатия")
            return False
        
        # 2. Рассчитываем новый битрейт для 70% от целевого размера
        new_bitrate = calculate_bitrate(max_size_mb * 0.7, duration)
        new_bitrate = max(400, new_bitrate)  # Минимальный битрейт
        print(f"ℹ️ Оптимизация с битрейтом: {new_bitrate}k")
        
        # 3. Более агрессивные параметры сжатия
        temp_file = input_file.with_stem(input_file.stem + "_opt")
        cmd = (
            f"ffmpeg -i '{input_file}' "
            "-c:v libx264 -profile:v baseline -level 3.0 "
            f"-b:v {new_bitrate}k -maxrate {new_bitrate}k -bufsize {new_bitrate * 2}k "
            "-pix_fmt yuv420p -vf 'scale=480:trunc(ow/a/2)*2' "  # Уменьшаем разрешение
            "-c:a aac -b:a 64k "  # Сильно уменьшаем аудио
            "-movflags +faststart "
            "-r 24 -g 48 -preset fast -crf 26 "  # Более агрессивное сжатие
            f"'{temp_file}'"
        )
        
        # 4. Запуск пережатия
        print("🔄 Пережатие...")
        subprocess.run(cmd, shell=True, check=True)
        
        # 5. Заменяем исходный файл
        if temp_file.exists():
            os.replace(temp_file, input_file)
            final_size = os.path.getsize(input_file) / (1024 * 1024)
            print(f"ℹ️ Финальный размер: {final_size:.2f} MB")
            return final_size <= max_size_mb
        
        return False
        
    except Exception as e:
        print(f"❌ Ошибка при пережатии: {str(e)}")
        if temp_file.exists():
            temp_file.unlink()
        return False

def batch_convert_directory(input_dir, output_dir, max_size_mb=90):
    """Пакетная конвертация с гарантированным контролем размера"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Поддерживаемые форматы
    formats = ['.mkv', '.mp4', '.avi', '.mov', '.flv', '.wmv']
    
    # Поиск видеофайлов
    video_files = []
    for ext in formats:
        video_files.extend(input_path.glob(f'*{ext}'))
    
    if not video_files:
        print("⚠️ Видеофайлы не найдены")
        return
    
    print(f"ℹ️ Найдено {len(video_files)} файлов для конвертации (макс. размер: {max_size_mb}MB)")
    
    # Конвертация
    success_count = 0
    for video_file in video_files:
        output_file = output_path / f"{video_file.stem}_ios6.mp4"
        print(f"\n🔹 Конвертация: {video_file.name} → {output_file.name}")
        
        if convert_to_ios6_compatible(video_file, output_file, max_size_mb):
            # Проверка размера
            size = os.path.getsize(output_file) / (1024 * 1024)
            if size <= max_size_mb:
                print(f"✅ Успешно! Размер: {size:.2f} MB")
                success_count += 1
            else:
                print(f"⚠️ Файл превышает лимит: {size:.2f} MB")
        else:
            print("❌ Ошибка конвертации")
            # Удаление битого файла
            if output_file.exists():
                output_file.unlink()
    
    print(f"\nℹ️ Готово! Успешно: {success_count}/{len(video_files)}")

def main():
    print("=== Конвертер видео для iOS 6 ===")
    print("Создает совместимые MP4 файлы ≤90MB для старых устройств Apple\n")
    
    input_dir = input("Введите путь к папке с исходными видео [текущая папка]: ").strip() or "."
    output_dir = input("Введите путь для сохранения результатов [ios6_videos]: ").strip() or "ios6_videos"
    
    if not os.path.isdir(input_dir):
        print(f"❌ Ошибка: папка не существует - {input_dir}")
        return
    
    # Создаем папку для результатов
    Path(output_dir).mkdir(exist_ok=True, parents=True)
    
    batch_convert_directory(input_dir, output_dir, max_size_mb=90)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {str(e)}")
    input("\nНажмите Enter для выхода...")
