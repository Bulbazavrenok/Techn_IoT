import json
import logging
from datetime import datetime
from typing import Set, Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from pydantic import BaseModel, field_validator
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String, Float, DateTime)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, insert, update, delete

from config import (POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)
import sys

# SQLAlchemy setup
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the ProcessedAgentData table
processed_agent_data = Table(
    "processed_agent_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("road_state", String),
    Column("agent_id", Integer),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("timestamp", DateTime))


# FastAPI models
class AccelerometerData(BaseModel):
    x: float
    y: float
    z: float


class GpsData(BaseModel):
    latitude: float
    longitude: float


class AgentData(BaseModel):
    agent_id: int
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime

    @classmethod
    @field_validator("timestamp", mode="before")
    def check_timestamp(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError(
                "Invalid timestamp format. Expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)."
            )


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData


# SQLAlchemy model  #Database model
class ProcessedAgentDataInDB(BaseModel):
    id: Optional[int] = -1
    road_state: str
    agent_id: int

    x: float
    y: float
    z: float

    latitude: float
    longitude: float
    timestamp: datetime


debug = False

# FastAPI app setup
app = FastAPI(debug=debug)

if debug:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        logging.error(f"{request}: {exc_str}")
        content = {'status_code': 10422, 'message': exc_str, 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

# WebSocket subscriptions
subscriptions: Dict[int, Set[WebSocket]] = {}
SessionLocal = sessionmaker(bind=engine)


# FastAPI WebSocket endpoint
@app.websocket("/ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: int):
    await websocket.accept()
    if agent_id not in subscriptions:
        subscriptions[agent_id] = set()
    subscriptions[agent_id].add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions[agent_id].remove(websocket)


# Function to send data to subscribed users
async def send_data_to_subscribers(agent_id: int, data):
    if agent_id in subscriptions:
        for websocket in subscriptions[agent_id]:
            await websocket.send_json(json.dumps(data))


# FastAPI CRUDL endpoints
@app.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    try:
        db_agent_data = SessionLocal()
        for item in data:
            road_state = item.road_state
            agent_data = item.agent_data
            agent_id = agent_data.agent_id
            accelerometer = agent_data.accelerometer
            gps = agent_data.gps
            timestamp = agent_data.timestamp
            query = insert(processed_agent_data).values(road_state=road_state, agent_id=agent_id, x=accelerometer.x,
                                                        y=accelerometer.y, z=accelerometer.z, latitude=gps.latitude,
                                                        longitude=gps.longitude, timestamp=timestamp)
            db_agent_data.execute(query)
            await send_data_to_subscribers(item.agent_data.agent_id, item.json())
        db_agent_data.commit()
    except Exception as e:
        db_agent_data.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db_agent_data.close()

    return {"message": "Success! Data created and sent to subscribers"}


@app.get(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB)
def read_processed_agent_data(processed_agent_data_id: int):
    try:
        db_agent_data = SessionLocal()
        query = select(processed_agent_data).where(processed_agent_data.c.id == processed_agent_data_id)
        data = db_agent_data.execute(query).fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail="Not found this data")
        return data
    finally:
        db_agent_data.close()


@app.get(
    "/processed_agent_data/",
    response_model=List[ProcessedAgentDataInDB])
def list_processed_agent_data():
    try:
        db_agent_data = SessionLocal()
        query = select(processed_agent_data)
        data = db_agent_data.execute(query).fetchall()
        return data
    finally:
        db_agent_data.close()


@app.put(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB)
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentData):
    try:
        db_agent_data = SessionLocal()
        road_state = data.road_state
        agent_data = data.agent_data
        agent_id = agent_data.agent_id
        accelerometer = agent_data.accelerometer
        gps = agent_data.gps
        timestamp = agent_data.timestamp
        update_query = (update(processed_agent_data)
                        .where(processed_agent_data.c.id == processed_agent_data_id)
                        .values(road_state=road_state, agent_id=agent_id, x=accelerometer.x, y=accelerometer.y,
                                z=accelerometer.z, latitude=gps.latitude, longitude=gps.longitude, timestamp=timestamp)
                        )
        db_agent_data.execute(update_query)
        db_agent_data.commit()
        updated_data = db_agent_data.execute(
            select(processed_agent_data).where(processed_agent_data.c.id == processed_agent_data_id)).fetchone()
        return updated_data
    except Exception as e:
        db_agent_data.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db_agent_data.close()


@app.delete(
    "/processed_agent_data/{processed_agent_data_id}",
    response_model=ProcessedAgentDataInDB)
def delete_processed_agent_data(processed_agent_data_id: int):
    try:
        db_agent_data = SessionLocal()
        delete_d = db_agent_data.execute(
            select(processed_agent_data).where(processed_agent_data.c.id == processed_agent_data_id)).fetchone()
        if delete_d is None:
            raise HTTPException(status_code=404, detail="Data not found")
        delete_query = delete(processed_agent_data).where(processed_agent_data.c.id == processed_agent_data_id)
        db_agent_data.execute(delete_query)
        db_agent_data.commit()
        return delete_d
    except Exception as e:
        db_agent_data.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db_agent_data.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
