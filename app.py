import requests
import os
import subprocess
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Maryland")

NAMESPACE = os.getenv("NAMESPACE", "default")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "your-app-deployment")

URL = f"https://api.openweathermap.org/data/2.5/weather?q={Nguti}&appid={383e2dc17ef71f1534ecdd274e447aff}"

def get_weather():
    response = requests.get(URL)
    data = response.json()
    return data["weather"][0]["main"].lower()

def scale_deployment(replicas):
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

@app.get("/")
def home():
    return {"message": "Weather Scaler Running"}

@app.get("/scale")
def scale():
    weather = get_weather()

    if "rain" in weather:
        scale_deployment(5)
        return {"weather": weather, "scaled_to": 5}
    else:
        scale_deployment(2)
        return {"weather": weather, "scaled_to": 2}


