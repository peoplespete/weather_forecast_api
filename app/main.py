'''Main API logic'''
from typing import Annotated
from datetime import datetime
from contextlib import asynccontextmanager
import pytz
import requests
import pickledb
from fastapi import FastAPI, HTTPException, Depends, Query
from apscheduler.schedulers.background import BackgroundScheduler

LAT = 41.8826
LON = -87.6233
REQUEST_TIMEOUT = 5
db = pickledb.load('tiny.db', False)

def fetch_forecast():
    '''Grabs lat/lng timestamped temperatures to aggregate values in key/value store'''
    points = requests.get(
        f'https://api.weather.gov/points/{LAT},{LON}',
        timeout=REQUEST_TIMEOUT
    ).json()
    forecasts = requests.get(
        points['properties']['forecastHourly'],
        timeout=REQUEST_TIMEOUT
    ).json()

    for i in range(72):
        forecast = forecasts['properties']['periods'][i]
        local_dt = datetime.strptime(forecast['startTime'], '%Y-%m-%dT%H:%M:%S%z')
        key = f'{LAT}-{LON}-{local_dt.astimezone(pytz.UTC)}'
        existing_values = db.get(key) or []
        existing_values.append(forecast['temperature'])
        db.set(key, existing_values)

def pad_hour(utc_hour: str) -> str:
    '''Adds leading zero if not present'''
    if len(utc_hour) == 1:
        return f'0{utc_hour}'
    return utc_hour

@asynccontextmanager
async def lifespan(_app):
    '''Makes sure that data collection happens in the background while FastAPI is running'''
    fetch_forecast()
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_forecast, 'interval', hours=1)
    scheduler.start()
    yield
    db.dump()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root(
    latitude: float,
    longitude: float,
    date: Annotated[str, Query(pattern=r'^\d{4}-\d{2}-\d{2}$')],
    utc_hour: Annotated[str, Depends(pad_hour)]
):
    '''Returns high/low temps based on stored forecast data given specific moment/location'''
    forecast_temps = db.get(f'{latitude}-{longitude}-{date} {utc_hour}:00:00+00:00')
    if isinstance(forecast_temps, list):
        return {
            'highest': max(forecast_temps),
            'lowest': min(forecast_temps),
        }
    raise HTTPException(status_code=404, detail='No data found')
