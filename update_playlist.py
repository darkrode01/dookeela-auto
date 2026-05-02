import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHANNELS = {
    "True Sport 7": "https://dookeela4.live/live-tv/tsp7",
    "Cartoon Network": "https://dookeela4.live/live-tv/cartoon-network"
}

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    # ใช้ chromedriver ที่ติดตั้งใน GitHub Actions
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver


def get_m3u8(url):
    driver = get_driver()

    try:
        print("🌐 Open:", url)
        driver.get(url)

        time.sleep(8)  # รอ player โหลด

        logs = driver.get_log("performance")

        for log in logs:
            msg = log["message"]

            if ".m3u8" in msg:
                start = msg.find("http")
                end = msg.find(".m3u8") + 5
                stream = msg[start:end]

                print("✅ FOUND:", stream)
                return stream

        print("❌ Not found")

    except Exception as e:
        print("🔥 ERROR:", str(e))

    finally:
        driver.quit()

    return None


playlist = {
    "name": "GOD PLAYLIST",
    "groups": [
        {
            "name": "LIVE",
            "stations": []
        }
    ]
}

for name, url in CHANNELS.items():
    stream = get_m3u8(url)

    if stream:
        playlist["groups"][0]["stations"].append({
            "name": name,
            "url": stream
        })


with open("playlist.json", "w", encoding="utf-8") as f:
    json.dump(playlist, f, ensure_ascii=False, indent=2)

print("🔥 DONE")
