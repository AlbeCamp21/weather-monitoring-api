from fastapi import FastAPI, HTTPException
import httpx
import psycopg2
import os
from datetime import datetime

app = FastAPI(title="Weather Monitoring API", version="1.0.0")

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "weather_monitoring"),
        user=os.getenv("DB_USER", "weather_user"),
        password=os.getenv("DB_PASSWORD", "weather_password")
    )

@app.get("/")
def read_root():
    return {"message": "Weather Monitoring API"}

@app.get("/health")
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "healthy", "timestamp": datetime.now()}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database connection failed")

@app.get("/weather/{city}")
async def get_weather(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            )
            weather_data = response.json()
            
            if response.status_code == 200:
                # Store in database
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO weather_data (city, temperature, humidity, description) VALUES (%s, %s, %s, %s)",
                    (city, weather_data["main"]["temp"], weather_data["main"]["humidity"], weather_data["weather"][0]["description"])
                )
                conn.commit()
                conn.close()
                
                return {
                    "city": city,
                    "temperature": weather_data["main"]["temp"],
                    "humidity": weather_data["main"]["humidity"],
                    "description": weather_data["weather"][0]["description"]
                }
            else:
                raise HTTPException(status_code=404, detail="City not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{city}")
def get_weather_history(city: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT temperature, humidity, description, timestamp FROM weather_data WHERE city = %s ORDER BY timestamp DESC LIMIT 10",
            (city,)
        )
        records = cursor.fetchall()
        conn.close()
        
        return {
            "city": city,
            "history": [
                {
                    "temperature": record[0],
                    "humidity": record[1],
                    "description": record[2],
                    "timestamp": record[3]
                }
                for record in records
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))