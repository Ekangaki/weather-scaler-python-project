import requests
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Maryland")

NAMESPACE = os.getenv("NAMESPACE", "default")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "Maryland_weather_App")

URL = f"https://api.openweathermap.org/data/2.5/weather?q={Maryland}&appid={383e2dc17ef71f1534ecdd274e447aff}"

def get_weather():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data["weather"][0]["main"].lower()
    except Exception as e:
        print("Weather fetch error:", e)
        return None

def scale_deployment(replicas):
    try:
        subprocess.run(
            [
                "kubectl",
                "scale",
                "deployment",
                DEPLOYMENT_NAME,
                f"--replicas={replicas}",
                "-n",
                NAMESPACE,
            ],
            check=True,
        )
        print(f"Scaled to {replicas} replicas.")
    except subprocess.CalledProcessError as e:
        print("Scaling failed:", e)

def main():
    weather = get_weather()

    if weather:
        print("Current weather:", weather)

        if "rain" in weather:
            print("Rain detected → Scaling to 5 pods")
            scale_deployment(5)
        else:
            print("No rain → Scaling to 2 pods")
            scale_deployment(2)

if __name__ == "__main__":
    main()
