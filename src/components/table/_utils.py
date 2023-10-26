import base64
import random
import asyncio
import subprocess
import json
import string
import uuid
import asyncio
import os
import signal
import psutil
import time
import zipfile
import shutil
import wmi
import winreg


def getFolderCache():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\MktBrowser")
        value, regtype = winreg.QueryValueEx(key, "pathMktCache")
        winreg.CloseKey(key)
        return value
    except:
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\MktBrowser")
            winreg.SetValueEx(key, "pathMktCache", 0, winreg.REG_SZ, createFolderCache())
            value, regtype = winreg.QueryValueEx(key, "pathMktCache")
            winreg.CloseKey(key)
            return value
        except:
            pass


def createFolderCache():
    c = wmi.WMI(namespace="cimv2")
    partitions = c.Win32_LogicalDisk()
    partitions = sorted(partitions, key=lambda p: p.FreeSpace, reverse=True)
    largest_partition = partitions[0]
    # #print(f"Largest partition: {largest_partition.Caption}, Free space: {int(largest_partition.FreeSpace) / (1024*1024*1024):.2f} GB")
    mktFolder = os.path.join(largest_partition.Caption, ".MktBrowser")
    mktCacheFolder = os.path.join(mktFolder, "Cache")
    os.makedirs(mktFolder, exist_ok=True)
    os.system(f"attrib +h {mktFolder}")
    os.makedirs(mktCacheFolder, exist_ok=True)
    os.system(f"attrib +h {mktCacheFolder}")


def waitUntilProfileUsing(profile_path, try_count=0):
    if try_count > 10:
        return
    time.sleep(1)
    _profile_path = profile_path
    if os.path.exists(profile_path):
        try:
            os.rename(_profile_path, _profile_path)
        except OSError as e:
            #print("waiting chrome termination")
            waitUntilProfileUsing(try_count + 1)


def stop(pid):
    for proc in psutil.process_iter(['pid']):
        if proc.info.get('pid') == pid:
            proc.kill()
    waitUntilProfileUsing()


def extractProfileZip(empty_profile, profile_zip_path, profile_path):
    shutil.copy(empty_profile, profile_zip_path)
    with zipfile.ZipFile(profile_zip_path, 'r') as zip_ref:
        zip_ref.extractall(profile_path)
    os.remove(profile_zip_path)


def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        #print(f"Process with PID {pid} has been terminated.")
    except OSError:
        #print(f"Unable to terminate process with PID {pid}.")


def is_valid_pid(pid):
    if not isinstance(pid, int) or pid < 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


async def delay(seconds):
    await asyncio.sleep(seconds)


def createGUID():
    return str(uuid.uuid4()).replace("-", "")


def random_string(length, characters=string.ascii_letters):
    return ''.join(random.choice(characters) for i in range(length))


def encodeBase64(config):
    str1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    str2 = "hTy1bfRJz4nLPcBCO7WtmNIaGvVeul5Zo8kq32UxrYw_-0gsjp96SDFXQiEMKdHA"
    bytes = config.encode('utf-8')
    base64data = base64.b64encode(bytes).decode('utf-8')
    s = ""
    for e in base64data:
        t = str1.find(e)
        s += e if t < 0 else str2[t:t + 1]
    return s


def decodeBase64(hash):
    str1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    str2 = "hTy1bfRJz4nLPcBCO7WtmNIaGvVeul5Zo8kq32UxrYw_-0gsjp96SDFXQiEMKdHA"
    s = ""
    for e in hash:
        t = str2.find(e)
        s += e if t < 0 else str1[t:t + 1]
    bytes = base64.b64decode(s)
    return json.loads(bytes.decode('utf-8'))


def createmediaDevices(e):
    t = []
    n = [
        {
            "input": "Microphone Array (2- Realtek High Definition Audio)",
            "output": "Speaker/Headphone (2- Realtek High Definition Audio)"
        },
        {
            "input": "Microphone Array (Realtek High Definition Audio)",
            "output": "Speaker/Headphone (Realtek High Definition Audio)"
        },
        {
            "input": "Microphone Array (Realtek(R) Audio)",
            "output": "Speaker (Realtek(R) Audio)"
        },
        {
            "input": "Microphone Array (Conexant SmartAudio HD)",
            "output": "Speaker (Conexant SmartAudio HD)"
        },
        {
            "input": "Microphone Array (2- Conexant SmartAudio HD)",
            "output": "Speaker (2- Conexant SmartAudio HD)"
        },
        {
            "input": "Microphone Array (Synaptics Audio)",
            "output": "Speaker (Synaptics Audio)"
        }
    ]
    r = ""
    a = 0
    for i in range(len(e)):
        a += ord(e[i])
        r += format(a, "x")
    o = r[:4]
    s = r[-4:]
    l = ["c", "d", "e", "f"]
    if len(o) < 4:
        for i in range(4 - len(o)):
            o += l[i]
            s += l[-(i + 1)]
    c = n[a % len(n)] if len(n) > 0 else {"input": "", "output": ""}
    t.append({"kind": "audioinput", "label": c["input"]})
    t.append({"kind": "videoinput", "label": f"Integrated Camera ({o}:{s})"})
    t.append({"kind": "audiooutput", "label": c["output"]})
    return t


def genMAC():
    hexDigits = "0123456789ABCDEF"
    macAddress = ""
    for i in range(6):
        macAddress += hexDigits[random.randint(0, 15)]
        macAddress += hexDigits[random.randint(0, 15)]
        if i != 5:
            macAddress += "-"
    return macAddress


def check_port_available(port):
    try:
        result = subprocess.run(
            f"netstat -aon | find \"{port}\"", capture_output=True, shell=True)
        if result.stdout:
            return False
    except Exception as e:
        #print(e)
    return True


def get_random_int(min_val, max_val):
    return random.randint(min_val, max_val)


def get_random_port():
    port = get_random_int(20000, 40000)
    port_available = check_port_available(port)
    while not port_available:
        port = get_random_int(20000, 40000)
        port_available = check_port_available(port)
    return port
