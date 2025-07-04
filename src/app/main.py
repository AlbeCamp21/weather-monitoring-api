import os
import httpx
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Variables necesarias
API_KEY = os.getenv("API_KEY")
CITY = os.getenv("CITY", "Lima")
UNITS = os.getenv("UNITS", "metric")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data():
    """
    Consulta la API de OpenWeatherMap y devuelve datos relevantes.
    """
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": UNITS
    }

    try:
        response = httpx.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "timestamp": data["dt"]
        }

        return weather_info

    except httpx.RequestError as exc:
        print(f"[ERROR] Error de conexión: {exc}")
        return None

    except httpx.HTTPStatusError as exc:
        print(f"[ERROR] Código de estado HTTP: {exc.response.status_code}")
        return None

    except KeyError:
        print("[ERROR] Error al procesar los datos de respuesta")
        return None

def test_connection():
    """
    Prueba rápida para verificar conexión con la API.
    """
    print("[INFO] Probando conexión con OpenWeatherMap...")
    result = get_weather_data()
    if result:
        print("[SUCCESS] Conexión exitosa.")
        print(result)
    else:
        print("[FAIL] No se pudo obtener datos del clima.")

if __name__ == "__main__":
    test_connection()