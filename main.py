import time
import requests
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw, ImageFont
import sys
import threading

def load_font(size):
    return ImageFont.truetype("fa-solid-900.otf", size)

def create_status_icon(status):
    width, height = 24, 24
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = load_font(size=18)
    status_icons = {
        "free": "\uf0c0",
        "busy": "\uf110",
        "not-available": "\uf00d",
        "bored": "\uf118",
        "sleep": "\uf186",
    }
    icon_char = status_icons.get(status, "\uf128")
    text_bbox = draw.textbbox((0, 0), icon_char, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), icon_char, font=font, fill="white")
    return image

def update_text(icon):
    last_status = None
    try:
        while True:
            response = requests.get('https://status.philiploebl.com/api/update/current/')
            data = response.json()
            status_name = data['data']['status']['name']
            if status_name != last_status:
                icon.icon = create_status_icon(status_name)
                icon.notify(f"Status updated to: {status_name}")
                last_status = status_name
            time.sleep(5)
    except Exception as e:
        icon.stop()
        sys.exit(1)

menu = Menu(MenuItem("Quit", lambda icon: icon.stop()))
icon = Icon("TaskbarText", create_status_icon("default"), "Status Monitor", menu)
updater_thread = threading.Thread(target=update_text, args=(icon,), daemon=True)
updater_thread.start()
icon.run()
