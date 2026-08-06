import requests
import time
from datetime import datetime
import winsound
import threading
import sys

URL = "https://data.moenv.gov.tw/api/v2/aqx_p_02"
THRESHOLD = 35
CHECK_INTERVAL = 900  # 15 分鐘

# 可監測城市清單
CITY_LIST = [
    "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣",
    "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣",
    "臺南市", "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣",
    "澎湖縣", "金門縣", "連江縣"
]

shutdown_event = threading.Event()


def get_latest_pm25_data(api_key, target_county):
    params = {
        "format": "json",
        "limit": 1000,
        "sort": "datacreationdate desc",
        "api_key": api_key
    }

    try:
        response = requests.get(URL, params=params, timeout=20)
    except Exception as e:
        print("連線失敗：", e)
        return None

    if response.status_code != 200:
        print("API 回應失敗")
        print("狀態碼：", response.status_code)
        print("回傳內容：", response.text)
        return None

    try:
        data = response.json()
    except Exception:
        print("JSON 解析失敗")
        print(response.text)
        return None

    city_data = [item for item in data if item.get("county", "").strip() == target_county]

    latest_by_site = {}

    for item in city_data:
        site = item.get("site", "").strip()
        pm25 = item.get("pm25", "").strip()
        dt = item.get("datacreationdate", "").strip()

        if not site or not pm25 or not dt:
            continue

        try:
            pm25_num = float(pm25)
            dt_obj = datetime.strptime(dt, "%Y-%m-%d %H:%M")
        except Exception:
            continue

        if site not in latest_by_site or dt_obj > latest_by_site[site]["time"]:
            latest_by_site[site] = {
                "site": site,
                "pm25": pm25_num,
                "unit": item.get("itemunit", ""),
                "time": dt_obj,
                "time_str": dt
            }

    latest_data = list(latest_by_site.values())
    latest_data.sort(key=lambda x: x["pm25"], reverse=True)

    return latest_data


def show_monitor_result(target_county, latest_data):
    if not latest_data:
        print(f"找不到 {target_county} 的資料")
        return

    print("\n" + "=" * 60)
    print(f"{target_county} PM2.5 即時監測")
    print("檢查時間:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    for item in latest_data:
        warn = " ⚠️超標" if item["pm25"] >= THRESHOLD else ""
        print(
            f"測站:{item['site']:<10}"
            f"PM2.5:{item['pm25']:<6}"
            f"{item['unit']:<8}"
            f"時間:{item['time_str']}{warn}"
        )

    print("-" * 60)

    highest = latest_data[0]
    print("最高測站:", highest["site"])
    print("PM2.5:", highest["pm25"], highest["unit"])
    print("資料時間:", highest["time_str"])

    if highest["pm25"] >= THRESHOLD:
        print("\n⚠️⚠️⚠️ 空氣品質警告 ⚠️⚠️⚠️")
        print("PM2.5 已超過", THRESHOLD)
        print("測站:", highest["site"])
        print("PM2.5:", highest["pm25"])
        winsound.Beep(2000, 1000)
    else:
        print("目前未超過警戒值")


def show_city_list():
    print("\n可監測城市清單：")
    print("-" * 30)
    for i, city in enumerate(CITY_LIST, start=1):
        print(f"{i}. {city}")
    print("-" * 30)


def listen_for_commands(stop_event, update_event, current_city):
    while not stop_event.is_set() and not shutdown_event.is_set():
        user_input = input().strip().lower()

        if user_input == "stop":
            stop_event.set()
            update_event.set()
            print("\n監測已停止，返回主選單。\n")

        elif user_input == "change":
            new_city = input("請輸入新的監測城市：").strip()

            if new_city not in CITY_LIST:
                print("城市名稱不在清單中，請輸入 city 查看可用城市。")
            else:
                current_city["name"] = new_city
                update_event.set()   # 立刻通知主迴圈更新
                print(f"\n監測城市已更改為：{new_city}，正在立即更新資料...\n")

        elif user_input == "city":
            show_city_list()

        elif user_input == "shutdown":
            shutdown_event.set()
            stop_event.set()
            update_event.set()
            print("\n系統關閉中...\n")
            break

        elif user_input != "":
            print("監測中可輸入 stop、change、city 或 shutdown")

def start_monitor(api_key, target_county):
    stop_event = threading.Event()
    update_event = threading.Event()
    current_city = {"name": target_county}

    print(f"\n開始監測 {current_city['name']}")
    print("每 15 分鐘更新一次")
    print("輸入 stop 停止監測")
    print("輸入 change 更換監測城市")
    print("輸入 city 查看城市清單")
    print("輸入 shutdown 關閉程式\n")

    listener_thread = threading.Thread(
        target=listen_for_commands,
        args=(stop_event, update_event, current_city),
        daemon=True
    )
    listener_thread.start()

    while not stop_event.is_set() and not shutdown_event.is_set():
        update_event.clear()

        latest_data = get_latest_pm25_data(api_key, current_city["name"])

        if latest_data is not None:
            show_monitor_result(current_city["name"], latest_data)

        if stop_event.is_set() or shutdown_event.is_set():
            break

        print("\n等待 15 分鐘後更新")
        print("監測中可輸入：stop / change / city / shutdown\n")

        # 等待 900 秒，但如果 change/stop/shutdown 發生，就立刻跳出等待
        update_event.wait(timeout=CHECK_INTERVAL)

def main():
    print("===== PM2.5 即時監測系統 =====")

    api_key = input("請輸入 API Key：").strip()
    if not api_key:
        print("API Key 不可為空")
        return

    current_city = None   # 記住上一次監測城市

    while not shutdown_event.is_set():
        print("\n主選單可輸入：start / city / change / shutdown")

        if current_city:
            print(f"目前預設城市：{current_city}")
        else:
            print("目前預設城市：尚未設定")

        command = input("請輸入指令：").strip().lower()

        if command == "start":
            if current_city is None:
                city = input("請輸入監測城市（先輸入 city 可查看清單）：").strip()

                if city not in CITY_LIST:
                    print("城市名稱不在清單中，請先輸入 city 查看可用城市。")
                    continue

                current_city = city

            start_monitor(api_key, current_city)

        elif command == "change":
            city = input("請輸入新的監測城市：").strip()

            if city not in CITY_LIST:
                print("城市名稱不在清單中，請先輸入 city 查看可用城市。")
                continue

            current_city = city
            print(f"預設城市已更改為：{current_city}")

        elif command == "city":
            show_city_list()

        elif command == "shutdown":
            shutdown_event.set()
            print("系統已關閉")

        else:
            print("無效指令，請輸入 start、city、change 或 shutdown")

    sys.exit()


if __name__ == "__main__":
    main()