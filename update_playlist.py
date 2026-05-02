import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHANNELS = {
    "True Sport 7": "https://dookeela4.live/live-tv/tsp7",
    "Cartoon Network": "https://dookeela4.live/live-tv/cartoon-network"
}

def get_m3u8(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(8)  # รอ player โหลด

        logs = driver.get_log("performance")

        for log in logs:
            message = log["message"]

            if ".m3u8" in message:
                start = message.find("http")
                end = message.find(".m3u8") + 5
                return message[start:end]

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

    return None


playlist = {
    "name": "AUTO GOD PLAYLIST",
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
