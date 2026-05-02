import requests
import re
import json

# รายชื่อช่องและ URL หน้าเว็บของ dookeela
CHANNELS = {
    "True Sport 7": "https://dookeela4.live/live-tv/tsp7",
    "Animal Show": "https://dookeela4.live/live-tv/animalshow",
    "สำรวจโลก": "https://dookeela4.live/live-tv/samruilok",
    "Cartoon Network": "https://dookeela4.live/live-tv/cartoon-network",
    "Nickelodeon": "https://dookeela4.live/live-tv/nickelodeon"
}

def get_stream_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)

        # ใช้ Regex ค้นหาลิงก์ m3u8
        match = re.search(r'https?://live[12]\.stream\.liveplayback\.net/[^"\']+', response.text)

        if match:
            return match.group(0)

    except Exception as e:
        print("Error:", e)

    return None


# โครงสร้าง JSON หลัก
playlist = {
    "name": "Auto Update Playlist",
    "author": "Gemini Bot",
    "image": "https://raw.githubusercontent.com/nookkiir5r5-png/-/refs/heads/main/images.jpeg",
    "groups": [
        {
            "name": "Auto Updated Channels",
            "stations": []
        }
    ]
}

# วนลูปดึง stream
for name, url in CHANNELS.items():
    stream_url = get_stream_url(url)

    if stream_url:
        playlist["groups"][0]["stations"].append({
            "name": name,
            "url": stream_url,
            "referer": "https://dookeela4.live/",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "playInNatPlayer": True
        })

# บันทึกเป็นไฟล์ JSON
with open('playlist.json', 'w', encoding='utf-8') as f:
    json.dump(playlist, f, ensure_ascii=False, indent=2)

print("✅ สร้าง playlist.json สำเร็จ")
