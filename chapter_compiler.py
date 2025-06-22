import requests
from concurrent.futures import ThreadPoolExecutor
import time

def check_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=5,
            allow_redirects=False
        )
        if response.status_code != 200:
            print(f"Недоступна: {url} (Код: {response.status_code})")
            return url
        # Проверка на страницу DDOS Guard (если код 200, но контент содержит проверку)
        if "ddos" in response.text.lower() or "cloudflare" in response.text.lower():
            print(f"DDOS Guard защита: {url}")
            return url
    except requests.RequestException as e:
        print(f"Ошибка: {url} ({str(e)})")
        return url
    return None

def check_all_urls(urls):
    unavailable_urls = []
    with ThreadPoolExecutor(max_workers=5) as executor:  # Уменьшил число потоков
        results = executor.map(check_url, urls)
        for result in results:
            if result:
                unavailable_urls.append(result)
            time.sleep(0.5)  # Задержка между запросами
    return unavailable_urls

if __name__ == "__main__":
    with open('grand_blue_images.txt', 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    
    print("Проверка URL...")
    unavailable = check_all_urls(urls)
    
    print("\nРезультат:")
    if unavailable:
        print(f"Недоступно: {len(unavailable)} URL")
        for url in unavailable:
            print(url)
    else:
        print("Все URL доступны.")