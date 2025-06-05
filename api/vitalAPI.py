from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.path.join(BASE_DIR, "PINT.db")

class RecordsData(BaseModel):
    """
    Defines the structure of the record table 
    """
    device_id: str
    record_date: str
    steps: Optional[int] = None 
    heartrate: Optional[float] = None  
    avg_heartrate: Optional[float] = None
    peak_heartrate: Optional[float] = None
    oxygen: Optional[float] = None  
    avg_oxygen: Optional[float] = None
    humidity: Optional[float] = None
    avg_humidity: Optional[float] = None
    temp: Optional[float] = None
    avg_temp: Optional[float] = None
    co2: Optional[int] = None
    avg_co2: Optional[int] = None 
    lat: Optional[float] = None
    lon: Optional[float] = None
    emerg: Optional[int] = None
    
# class LocationData(BaseModel):
#     """Defines the structure of the location table"""    
#     device_id: str
#     lat: str 
#     lon: str

class UserLocation(BaseModel):
    """Defines the structure to retrieve user's location"""
    device_id: str
    lat: str
    lon: str

app = FastAPI()

def get_db():
    """ Get information from DataBase"""
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    try:
        yield con 
    finally:
        con.close()    


@app.get('/')
async def root():
    return {
        "Status": "successful",
        "Instructions": [
            "For patient record use: /records in url"
            "For patient location use: /locations in url"
        ]
    }

@app.get('/records', response_model=List[RecordsData])
async def records(
    device_id: Optional[str] = None,
    record_date: Optional[str] = None,
    steps: Optional[int] = None, 
    heartrate: Optional[float] = None, 
    avg_heartrate: Optional[float] = None,
    peak_heartrate: Optional[float] = None,
    oxygen: Optional[float] = None,  
    avg_oxygen: Optional[float] = None,
    humidity: Optional[float] = None,
    avg_humidity: Optional[float] = None, 
    temp: Optional[float] = None, 
    avg_temp: Optional[float] = None, 
    co2: Optional[int] = None, 
    avg_co2: Optional[int] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None, 
    emerg: Optional[int] = None,
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    #cursor.execute(device_id, record_time, steps, heartrate, oxygen)
    cursor.execute("SELECT * FROM records")
    data = cursor.fetchall()
    return[
        RecordsData(
            device_id=row['device_id'], 
            record_date=row['record_date'],
            steps=row['steps'],
            heartrate=row['heartrate'],
            avg_heartrate=row['avg_heartrate'],
            peak_heartrate=row['peak_heartrate'],
            oxygen=row['oxygen'],
            avg_oxygen=row['avg_oxygen'],
            humidity=row['humidity'],
            avg_humidity=row['avg_humidity'],
            temp=row['temp'],
            avg_temp=row['avg_temp'],
            co2=row['co2'],
            avg_co2=row['avg_co2'],
            lat=row['lat'],
            lon=row['lon'],
            emerg=row['emerg']
        ) for row in data
    ]

# @app.get('/locations', response_model=List[LocationData])
# def locations(
#     device_id: Optional[str] = None,
#     lat: Optional[str] = None, 
#     lon: Optional[str] = None,
#     db: sqlite3.Connection = Depends(get_db)
# ):
#     cur = db.cursor()
#     cur.execute("SELECT * FROM locations")
#     data = cur.fetchall()
#     return[
#         LocationData(
#             device_id=row['device_id'], 
#             lat=row['lat'], 
#             lon=row['lon']
#         ) for row in data
#     ]


# @app.post('/user_location')
# async def retrieve_user_location (location: UserLocation):
     
#     with sqlite3.connect('PINT.db') as db:
#         print(location.device_id, location.lat, location.lon)
#         cur = db.cursor()
#         cur.execute("INSERT INTO locations (device_id, lat, lon) VALUES (?, ?, ?)", (location.device_id, location.lat, location.lon))
#         db.commit()
#     print(f"Data inserted: device_id{location.device_id}, lat{location.lat}, lon{location.lon}")
#     return{"status": "successful",
#            "data": location.model_dump()}

@app.get("/debug")
def debug():
    import os
    return {
        "exists": os.path.exists("PINT.db"),
        "size": os.path.getsize("PINT.db") if os.path.exists("PINT.db") else 0
    }


#uvicorn vitalAPI:app --reload