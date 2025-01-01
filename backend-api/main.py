from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Client, Order, Route, RouteStep
from genetic import run_genetic

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/vrptw"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

class ClientInput(BaseModel):
    name: str
    address: str
    lat: float
    lng: float
    delivery_deadline: str

class RouteOutput(BaseModel):
    route: List[int]
    fitness: float

@app.post("/clients")
def create_client(client: ClientInput):
    db = SessionLocal()
    new_client = Client(
        name=client.name,
        address=client.address,
        lat=str(client.lat),
        lng=str(client.lng),
        delivery_deadline=client.delivery_deadline
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    db.close()
    return {"client_id": new_client.id}

@app.get("/clients")
def list_clients():
    db = SessionLocal()
    clients = db.query(Client).all()
    db.close()
    return clients

@app.post("/compute_route", response_model=RouteOutput)
def compute_route(client_ids: List[int]):
    db = SessionLocal()
    clients = db.query(Client).filter(Client.id.in_(client_ids)).all()
    coords = [(float(c.lat), float(c.lng)) for c in clients]
    solution, fitness = run_genetic(coords)
    new_route = Route(route_data={"solution": list(solution)}, start_location=None, end_location=None)
    db.add(new_route)
    db.commit()
    for idx, s in enumerate(solution):
        step = RouteStep(route_id=new_route.id, step_index=idx, client_id=clients[s].id)
        db.add(step)
    db.commit()
    db.close()
    return {"route": list(solution), "fitness": fitness}
