from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

class RecordsData(BaseModel):
    """
    Defines the structure of the record table 
    """
    device_id: str
    record_time: str
    steps: Optional[int] = None 
    heartrate: Optional[int] = None  
    oxygen: Optional[int] = None  
    
class LocationData(BaseModel):
    """Defines the structure of the location table"""    
    device_id: str
    lat: str 
    lon: str

class UserLocation(BaseModel):
    """Defines the structure to retrieve user's location"""
    device_id: str
    lat: str
    lon: str

app = FastAPI()

def get_db():
    """ Get information from DataBase"""
    con = sqlite3.connect('PINT.db')
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
def records(
    device_id: Optional[str] = None,
    record_time: Optional[str] = None,
    steps: Optional[int] = None, 
    heartrate: Optional[int] = None, 
    oxygen: Optional[int] = None,  
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    #cursor.execute(device_id, record_time, steps, heartrate, oxygen)
    cursor.execute("SELECT * FROM records")
    data = cursor.fetchall()
    return[
        RecordsData(
            device_id=row['device_id'], 
            record_time=row['record_time'],
            steps=row['steps'],
            heartrate=row['heartrate'],
            oxygen=row['oxygen']
        ) for row in data
    ]

@app.get('/locations', response_model=List[LocationData])
def locations(
    device_id: Optional[str] = None,
    lat: Optional[str] = None, 
    lon: Optional[str] = None,
    db: sqlite3.Connection = Depends(get_db)
):
    cur = db.cursor()
    cur.execute("SELECT * FROM locations")
    data = cur.fetchall()
    return[
        LocationData(
            device_id=row['device_id'], 
            lat=row['lat'], 
            lon=row['lon']
        ) for row in data
    ]


@app.post('/user_location')
async def retrieve_user_location (location: UserLocation):
     
    with sqlite3.connect('PINT.db') as db:
        print(location.device_id, location.lat, location.lon)
        cur = db.cursor()
        cur.execute("INSERT INTO locations (device_id, lat, lon) VALUES (?, ?, ?)", (location.device_id, location.lat, location.lon))
        db.commit()
    print(f"Data inserted: device_id{location.device_id}, lat{location.lat}, lon{location.lon}")
    return{"status": "successful",
           "data": location.model_dump()}
#uvicorn vitalAPI:app --reload