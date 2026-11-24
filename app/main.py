from fastapi import FastAPI
from app.database import engine
from app import models

# Crée les tables dans la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini Réseau Social API",
    description="Une API de réseau social avec FastAPI",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API du Mini Réseau Social"}