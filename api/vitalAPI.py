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

class PatientData(BaseModel):
    """
    Defines the structure of the record table 
    """
    device_id: str
    record_date: str
    steps: Optional[int] = None 
    heartrate: Optional[float] = None  
    oxygen: Optional[float] = None  
    humidity: Optional[float] = None
    temp: Optional[float] = None
    co2: Optional[int] = None
    records_inserted: Optional[int] = None
    emerg: Optional[int] = None    
    

class UserLocation(BaseModel):
    """Defines the structure to retrieve user's location"""
    device_id: str
    record_date: str
    lat: float
    lon: float

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
            "For patient data records use: /records in url"
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
    cursor.execute("SELECT * FROM records")
    data = cursor.fetchall()
    return[
        RecordsData(
            device_id=row['device_id'], 
            record_date=row['record_date'],
            steps=row['steps'],
            heartrate=row['heartrate'],
            oxygen=row['oxygen'],
            humidity=row['humidity'],
            temp=row['temp'],
            co2=row['co2'],
            emerg=row['emerg']
        ) for row in data
    ]

@app.post('/user_location')
async def retrieve_user_location (location: UserLocation):
    with sqlite3.connect(DB_PATH) as db:
        # print(location.device_id, location.record_date, location.lat, location.lon)
        cur = db.cursor()
        cur = db.cursor()
        cur.execute("""INSERT INTO records (device_id, record_date, lat, lon) VALUES (?, ?, ?, ?)"
                    ON CONFLICT(device_id, record_date) DO UPDATE SET
                    lat = excluded.lat,
                    lon = excluded.lon
        """, 
        (location.device_id, location.record_date, location.lat, location.lon))
        db.commit()
    print(f"Data inserted: device_id{location.device_id}, record_date{location.record_date}, lat{location.lat}, lon{location.lon}")
    return{"status": "successful",
           "data": location.model_dump()}

    
@app.post('/user_data')
async def retrieve_user_data(data: PatientData):
    with sqlite3.connect(DB_PATH) as db:
        # print(data.device_id, data.record_date, data.steps, data.heartrate, data.avg_heartrate, data.peak_heartrate, data.oxygen, 
        #       data.avg_oxygen, data.humidity, data.avg_humidity, data.temp, data.avg_temp, data.co2, data.avg_co2, data.emerg)
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO records (
                device_id, record_date, steps, heartrate, avg_heartrate, peak_heartrate,
                oxygen, avg_oxygen, humidity, avg_humidity, temp, avg_temp,
                co2, avg_co2, records_inserted, emerg
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(device_id, record_date) DO UPDATE SET
            steps = excluded.steps,
            heartrate = excluded.heartrate,
            oxygen = excluded.oxygen,
            humidity = excluded.humidity,
            temp = excluded.temp,
            co2 = excluded.co2,
            emerg = excluded.emerg,
            avg_heartrate = ((records.avg_heartrate * records.records_inserted) + excluded.heartrate) / (records.records_inserted + 1),
            avg_oxygen    = ((records.avg_oxygen * records.records_inserted) + excluded.oxygen) / (records.records_inserted + 1),
            avg_humidity  = ((records.avg_humidity * records.records_inserted) + excluded.humidity) / (records.records_inserted + 1),
            avg_temp      = ((records.avg_temp * records.records_inserted) + excluded.temp) / (records.records_inserted + 1),
            avg_co2       = ((records.avg_co2 * records.records_inserted) + excluded.co2) / (records.records_inserted + 1),
            peak_heartrate = 
            CASE 
                WHEN excluded.heartrate > records.peak_heartrate THEN excluded.heartrate
                ELSE records.peak_heartrate
            END,
            records_inserted = records.records_inserted + 1
            """,
            (
                data.device_id, data.record_date, data.steps, data.heartrate, data.heartrate, data.heartrate, data.oxygen, data.oxygen, data.humidity, data.humidity,
                data.temp, data.temp, data.co2, data.co2, data.records_inserted, data.emerg
            )
        )
        db.commit()
        print(f"Data inserted: device_id{data.device_id}, record_data{data.record_date}, steps{data.steps}")
        # print(f"\n heartrate{data.heartrate}, avg_heartrate{data.avg_heartrate}, peak_heartrate{data.peak_heartrate}, oxygen{data.oxygen}, avg_oxygen")
        # print(f"\n humidity{data.humidity}, avg_humidity{data.avg_humidity}, temp{data.temp}, avg_temp{data.avg_temp}")
        # print(f"\n co2{data.co2}, avg_co2{data.avg_co2}, emerg{data.emerg}")
        return{"status": "successful",
               "data": data.model_dump()}    
#uvicorn vitalAPI:app --reload

#uvicorn vitalAPI:app --host 0.0.0.0 --port 8000 --reload