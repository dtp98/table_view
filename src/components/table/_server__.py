from threading import Thread
from functools import partial
from flask import Flask, jsonify, request
from controllers._browser_handler import *

app = Flask(__name__)
pids = []



@app.route('/api/start', methods=['POST'])
def start():
    # profile_backup = self._main_window.mktApi.get_backup_file_of_profile(id_profile)

    config = {
    "window_size": "840,1280",
    "verder": "Bao le Test verder.",
    "renderer": "Bao le Test renderer",
    "path_profiles": "F:\\mktlogin_2023\\browser\\Profiles",
    "name_profile": "profile_1",
    "path_chrome": "F:\\mktlogin_2023\\browser\\SunBrowser\\SunBrowser.exe",
    "id_Machine": "", # có thể bỏ trống
    "macAddress": "", # có thể bỏ trống
    "userId": "1", # Random
    "canvasMark": "9895", # 9500 => 9900
    "audioFp": 576, #-951
    "webGLMark": "6748", # 2600 => 6900 #3248
    "ipAddress": "174.243.149.176", # nếu dùng proxy thì check ip trước rồi thêm vô đây fake webrtc
    "ipLocalAddress": "174.243.149.176", # nếu dùng proxy thì check ip trước rồi thêm vô đây fake webrtc
    "proxyType": "socks5",
    "proxyHost": "",
    "proxyPort": 9043,
    "proxyUser": "notvn1.custom6",
    "proxyPass": "6722a71e9e",
    "timeZone": "America/Los_Angeles", # nếu dùng proxy thì check timezone trước rồi thêm vô đây
    "geoposition": "37.338221,-121.886331,1000", # nếu dùng proxy thì check location trước rồi thêm vô đây fake webrtc
    "userAgent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.119 Safari/537.36", # "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13; rv:106.0) Gecko/20010101 Firefox/106.0",//
    "platform": "Win32", # iPhone, Win32 , macOS
    "_platform": "Windows", # 'MacIntel' , Windows
    "architecture": "x86",
    "componentPreinstallPath": "G:\\.ADSPOWER_GLOBAL\\components\\108",
    "clientRectFp": 464, #-1887
    "hardwareConcurrency": 8,
    "deviceMemory": 32,
    "maxTouchPoints":10,
    "args": ["https://chat.zalo.me/"]
    }
    res = openProfileChrome(config)
    data = {'webSocketDebuggerUrl': res.get('webSocketDebuggerUrl'), 'pid':res.get('pid') }
    pids.append(res.get('pid'))
    return jsonify(data)

    # return jsonify(config)

@app.route('/api/stop-all', methods=['POST'])
def stop_all():
    data = request.get_json()
    for pid in pids:
       kill_process(pid)
    return jsonify({'result':True})

@app.route('/api/stop', methods=['POST'])
def stop():
    data = request.get_json()
    stop(data.get('pid'))
    return jsonify({'result':True})


async def start_flask_app():
    app.run(port=7195)

# flask_thread = Thread(target=start_flask_app, daemon=True)
# flask_thread.start()


if __name__ == "__main__":
    # Chạy asyncio trong một thread riêng biệt.
    loop = asyncio.new_event_loop()
    asyncio_thread = Thread(target=partial(loop.run_until_complete, start_flask_app()), daemon=True)
    asyncio_thread.start()