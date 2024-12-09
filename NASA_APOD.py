import requests
import json
from datetime import datetime, timedelta
import time

API_KEY = "syUrt9EdL5Ts0G5o9RU2jgQHF5QG9MrM0pg8jZqd"
API_ENDPOINT = "https://api.nasa.gov/planetary/apod"

def get_apod_info(api_key, date):
    try:
        response = requests.get(API_ENDPOINT, params={"api_key": api_key, "date": date})
        response.raise_for_status()
        data = response.json()
        return {"date": data.get("date"), "title": data.get("title"), "url": data.get("url"), "explanation": data.get("explanation"), "media_type": data.get("media_type")}
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching data for {date}: {e}")
        return None

def get_apod_data(api_key, s_date, e_date):
    start = datetime.strptime(s_date, "%Y-%m-%d")
    end = datetime.strptime(e_date, "%Y-%m-%d")

    try:
        current_date = start
        with open("apod_results.json", "a+") as file:
            if file.read(1):
                file.write(",\n")
            while current_date <= end:
                date_str = current_date.strftime("%Y-%m-%d")
                print(f"Acquiring data for {date_str}...")
                info = get_apod_info(api_key, date_str)
                if info:
                    json.dump(info, file, indent=4)
                    file.write(",\n")
                time.sleep(1)
                current_date += timedelta(days=1)
            file.seek(file.tell() - 2, 0)
            file.write("\n]")
    except Exception as e:
        print(f"An error occurred writing to the file: {e}")

def main():
    s_date = "2021-01-01"
    e_date = "2021-10-31"
    with open("apod_results.json", "w") as file:
        file.write("[\n")
    get_apod_data(API_KEY, s_date, e_date)
    print("Check the file for retrieved data.")

if __name__ == "__main__":
    main()
